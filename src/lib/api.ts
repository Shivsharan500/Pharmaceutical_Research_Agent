/**
 * API client for the pharmaceutical research backend
 */

// Configure your backend URL here
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

export interface StartResearchResponse {
  job_id: string;
  message: string;
}

export interface ResearchStatusResponse {
  job_id: string;
  molecule_name: string;
  status: 'pending' | 'running' | 'complete' | 'error';
  elapsed_seconds: number;
  result?: string;
  error?: string;
}

export interface ResearchResultResponse {
  job_id: string;
  molecule_name: string;
  result: string;
}

/**
 * Check if the backend server is running
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/health`);
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * Start a new research job for a molecule
 */
export async function startResearch(moleculeName: string): Promise<StartResearchResponse> {
  const response = await fetch(`${API_BASE_URL}/api/research/start`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ molecule_name: moleculeName }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to start research');
  }

  return response.json();
}

/**
 * Get the status of a research job
 */
export async function getResearchStatus(jobId: string): Promise<ResearchStatusResponse> {
  const response = await fetch(`${API_BASE_URL}/api/research/status/${jobId}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to get research status');
  }

  return response.json();
}

/**
 * Get the result of a completed research job
 */
export async function getResearchResult(jobId: string): Promise<ResearchResultResponse> {
  const response = await fetch(`${API_BASE_URL}/api/research/result/${jobId}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error || 'Failed to get research result');
  }

  return response.json();
}
