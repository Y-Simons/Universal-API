"use client";

import React, { useEffect, useMemo, useRef, useState } from 'react';
import { useParams } from 'next/navigation';

interface SignalMessage {
  type: 'join' | 'offer' | 'answer' | 'ice';
  senderId: string;
  sdp?: any;
  candidate?: any;
}

function uuid() {
  return Math.random().toString(36).slice(2) + Date.now().toString(36);
}

export default function TeleconsultRoom() {
  const params = useParams<{ room: string }>();
  const [messages, setMessages] = useState<string[]>([]);
  const [connected, setConnected] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const localId = useMemo(() => uuid(), []);
  const pcRef = useRef<RTCPeerConnection | null>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const localVideo = useRef<HTMLVideoElement | null>(null);
  const remoteVideo = useRef<HTMLVideoElement | null>(null);

  const sendSignal = (msg: SignalMessage) => {
    if (!wsRef.current) return;
    wsRef.current.send(JSON.stringify(msg));
  };

  useEffect(() => {
    if (!params?.room) return;
    const urlBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
    const wsUrl = urlBase.replace('http', 'ws') + `/teleconsult/ws/${params.room}`;
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;
    ws.onopen = () => {
      setMessages(prev => [...prev, 'Signalisation connectée']);
      sendSignal({ type: 'join', senderId: localId });
    };
    ws.onclose = () => setMessages(prev => [...prev, 'Signalisation fermée']);
    ws.onerror = () => setError('Erreur de socket');
    ws.onmessage = async (evt) => {
      try {
        const msg: SignalMessage = JSON.parse(evt.data);
        if (!msg || msg.senderId === localId) return; // ignore self
        if (!pcRef.current) return;
        if (msg.type === 'offer' && msg.sdp) {
          await pcRef.current.setRemoteDescription(new RTCSessionDescription(msg.sdp));
          const answer = await pcRef.current.createAnswer();
          await pcRef.current.setLocalDescription(answer);
          sendSignal({ type: 'answer', senderId: localId, sdp: answer });
        } else if (msg.type === 'answer' && msg.sdp) {
          await pcRef.current.setRemoteDescription(new RTCSessionDescription(msg.sdp));
        } else if (msg.type === 'ice' && msg.candidate) {
          try {
            await pcRef.current.addIceCandidate(new RTCIceCandidate(msg.candidate));
          } catch {}
        } else if (msg.type === 'join') {
          // If we are already set up, proactively offer to the new peer
          if (pcRef.current.localDescription) {
            const offer = await pcRef.current.createOffer();
            await pcRef.current.setLocalDescription(offer);
            sendSignal({ type: 'offer', senderId: localId, sdp: offer });
          }
        }
      } catch {
        // not a signaling JSON; optionally show as chat
        setMessages(prev => [...prev, evt.data]);
      }
    };
    return () => ws.close();
  }, [params?.room, localId]);

  const startMedia = async () => {
    try {
      const pc = new RTCPeerConnection({ iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] });
      pcRef.current = pc;
      pc.onicecandidate = (e) => {
        if (e.candidate) sendSignal({ type: 'ice', senderId: localId, candidate: e.candidate });
      };
      pc.ontrack = (ev) => {
        if (remoteVideo.current) remoteVideo.current.srcObject = ev.streams[0];
      };
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      if (localVideo.current) localVideo.current.srcObject = stream;
      stream.getTracks().forEach(t => pc.addTrack(t, stream));
      // As first mover, create an offer
      const offer = await pc.createOffer();
      await pc.setLocalDescription(offer);
      sendSignal({ type: 'offer', senderId: localId, sdp: offer });
      setConnected(true);
    } catch (e: any) {
      setError(e.message || 'Impossible de démarrer la caméra/micro');
    }
  };

  const stop = () => {
    try {
      pcRef.current?.getSenders().forEach(s => s.track?.stop());
      pcRef.current?.close();
    } catch {}
    pcRef.current = null;
    setConnected(false);
  };

  return (
    <div>
      <h2>Salon de téléconsultation: {params?.room}</h2>
      <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap' }}>
        <div>
          <h4>Local</h4>
          <video ref={localVideo} autoPlay playsInline muted style={{ width: 320, background: '#000' }} />
        </div>
        <div>
          <h4>Distant</h4>
          <video ref={remoteVideo} autoPlay playsInline style={{ width: 320, background: '#000' }} />
        </div>
      </div>
      <div style={{ marginTop: 12, display: 'flex', gap: 8 }}>
        {!connected ? <button onClick={startMedia}>Démarrer</button> : <button onClick={stop}>Arrêter</button>}
      </div>
      {error && <div style={{ color: 'red', marginTop: 8 }}>{error}</div>}
      <div style={{ border: '1px solid #ccc', padding: 8, height: 200, overflow: 'auto', marginTop: 12 }}>
        {messages.map((m, idx) => <div key={idx}>{m}</div>)}
      </div>
      <p style={{ marginTop: 12 }}>WebRTC 1:1 simplifié (STUN) utilisant la signalisation WS.</p>
    </div>
  );
}