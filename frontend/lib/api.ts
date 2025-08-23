export function apiBase() {
  return process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000';
}

export async function authFetch(path: string, init: RequestInit = {}) {
  const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  const headers = new Headers(init.headers || {});
  if (token) headers.set('Authorization', `Bearer ${token}`);
  if (!headers.has('Content-Type') && init.body) headers.set('Content-Type', 'application/json');
  const res = await fetch(`${apiBase()}${path}`, { ...init, headers });
  if (!res.ok) {
    const body = await res.json().catch(() => ({} as any));
    throw new Error(body?.detail || `Erreur ${res.status}`);
  }
  return res;
}