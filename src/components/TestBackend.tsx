// src/components/TestBackend.tsx
import { useEffect, useState } from 'react';
import api from '@/lib/api';

export function TestBackend() {
  const [status, setStatus] = useState<string>('Testing...');
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    const testConnection = async () => {
      try {
        // Test endpoint - adjust to your actual endpoint
        const response = await api.get('/cameras');
        setStatus('✅ Backend Connected!');
        setData(response.data);
        console.log('Backend response:', response.data);
      } catch (error: any) {
        setStatus('❌ Connection Failed');
        console.error('Backend error:', error.response?.data || error.message);
      }
    };

    testConnection();
  }, []);

  return (
    <div className="p-4 border rounded">
      <h2 className="text-lg font-bold">Backend Status</h2>
      <p>{status}</p>
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>}
    </div>
  );
}