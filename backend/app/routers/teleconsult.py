from typing import Dict, List

from fastapi import APIRouter, WebSocket, WebSocketDisconnect


router = APIRouter()


class ConnectionManager:
	def __init__(self) -> None:
		self.active_connections: Dict[str, List[WebSocket]] = {}

	async def connect(self, room: str, websocket: WebSocket) -> None:
		await websocket.accept()
		self.active_connections.setdefault(room, []).append(websocket)

	def disconnect(self, room: str, websocket: WebSocket) -> None:
		if room in self.active_connections:
			self.active_connections[room] = [ws for ws in self.active_connections[room] if ws != websocket]
			if not self.active_connections[room]:
				del self.active_connections[room]

	async def broadcast(self, room: str, message: str) -> None:
		for connection in self.active_connections.get(room, []):
			await connection.send_text(message)


manager = ConnectionManager()


@router.websocket("/ws/{room}")
async def websocket_endpoint(websocket: WebSocket, room: str) -> None:
	await manager.connect(room, websocket)
	try:
		while True:
			data = await websocket.receive_text()
			await manager.broadcast(room, data)
	except WebSocketDisconnect:
		manager.disconnect(room, websocket)