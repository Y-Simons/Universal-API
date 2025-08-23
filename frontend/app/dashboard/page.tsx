"use client";

import React, { useEffect, useMemo, useState } from 'react';
import { authFetch, apiBase } from '../../lib/api';

interface Patient {
  id: string;
  first_name: string;
  last_name: string;
  dob: string;
}

interface RiskScore {
  asa_class: number;
  risk_level: 'low' | 'moderate' | 'high' | 'very_high';
  score: number;
  rationale: string;
}

export default function DashboardPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      window.location.href = '/';
      return;
    }
    (async () => {
      try {
        const res = await authFetch(`/patients`);
        setPatients(await res.json());
      } catch (e: any) {
        setError(e.message);
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  const createConsult = async (patientId: string, type: 'preop' | 'postop') => {
    try {
      await authFetch(`/consultations/${type}/${patientId}`, { method: 'POST' });
      alert('Consultation créée');
    } catch (e: any) {
      alert(e.message);
    }
  };

  const viewRisk = async (patientId: string) => {
    try {
      const r = await authFetch(`/patients/${patientId}/risk`);
      const risk: RiskScore = await r.json();
      alert(`ASA ${risk.asa_class} - ${risk.risk_level} (score ${risk.score})\n${risk.rationale}`);
    } catch (e: any) {
      alert(e.message);
    }
  };

  if (loading) return <div>Chargement...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Patients</h2>
        <button onClick={() => { localStorage.removeItem('token'); window.location.href = '/'; }}>Se déconnecter</button>
      </div>
      <table style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr>
            <th style={{ textAlign: 'left', borderBottom: '1px solid #ddd', padding: 8 }}>Nom</th>
            <th style={{ textAlign: 'left', borderBottom: '1px solid #ddd', padding: 8 }}>Naissance</th>
            <th style={{ textAlign: 'left', borderBottom: '1px solid #ddd', padding: 8 }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {patients.map(p => (
            <tr key={p.id}>
              <td style={{ padding: 8 }}>{p.last_name} {p.first_name}</td>
              <td style={{ padding: 8 }}>{p.dob}</td>
              <td style={{ padding: 8, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                <button onClick={() => viewRisk(p.id)}>Score de risque</button>
                <button onClick={() => createConsult(p.id, 'preop')}>Créer pré-op</button>
                <button onClick={() => createConsult(p.id, 'postop')}>Créer post-op</button>
                <a href={`/teleconsult/${p.id}`}>Téléconsultation</a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}