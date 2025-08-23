"use client";

import React, { useState } from 'react';
import { apiBase } from '../lib/api';

export default function LoginPage() {
  const [email, setEmail] = useState('anesth@example.com');
  const [password, setPassword] = useState('changeme');
  const [error, setError] = useState<string | null>(null);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      const res = await fetch(`${apiBase()}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body?.detail || 'Échec de connexion');
      }
      const data = await res.json();
      localStorage.setItem('token', data.access_token);
      window.location.href = '/dashboard';
    } catch (err: any) {
      setError(err.message || 'Erreur');
    }
  };

  return (
    <div style={{ maxWidth: 420 }}>
      <h2>Connexion</h2>
      <form onSubmit={onSubmit}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
          <label>
            Email
            <input value={email} onChange={e => setEmail(e.target.value)} type="email" style={{ width: '100%', padding: 8 }} />
          </label>
          <label>
            Mot de passe
            <input value={password} onChange={e => setPassword(e.target.value)} type="password" style={{ width: '100%', padding: 8 }} />
          </label>
          {error && <div style={{ color: 'red' }}>{error}</div>}
          <button type="submit" style={{ padding: '8px 12px' }}>Se connecter</button>
        </div>
      </form>
    </div>
  );
}