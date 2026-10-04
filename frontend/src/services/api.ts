import { InvestigationResult } from '../types';

const API_BASE = '/api';

export async function investigateText(text: str): Promise<InvestigationResult> {
  const resp = await fetch(`${API_BASE}/investigations/text`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  });
  if (!resp.ok) throw new Error('Investigation request failed');
  return resp.json();
}

export async function investigateImage(file: File): Promise<InvestigationResult> {
  const formData = new FormData();
  formData.append('file', file);
  const resp = await fetch(`${API_BASE}/investigations/image`, {
    method: 'POST',
    body: formData,
  });
  if (!resp.ok) throw new Error('Image OCR investigation failed');
  return resp.json();
}

export async function investigateAudio(file: File): Promise<InvestigationResult> {
  const formData = new FormData();
  formData.append('file', file);
  const resp = await fetch(`${API_BASE}/investigations/audio`, {
    method: 'POST',
    body: formData,
  });
  if (!resp.ok) throw new Error('Audio ASR investigation failed');
  return resp.json();
}

export async function runDemoScenario(): Promise<InvestigationResult> {
  const resp = await fetch('/demo');
  if (!resp.ok) throw new Error('Demo scenario failed');
  return resp.json();
}

export async function fetchDashboardStats(): Promise<any> {
  const resp = await fetch(`${API_BASE}/dashboard/stats`);
  if (!resp.ok) return { total_investigations: 0, high_risk_interceptions: 0 };
  return resp.json();
}
