import { useState, useCallback } from 'react';
import api from '../services/api';
import { useToast } from '../context/ToastContext';

export function useApi() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { addToast } = useToast();

  const execute = useCallback(async (fn, errorMsg = 'Operation failed') => {
    setLoading(true);
    setError(null);
    try {
      const result = await fn();
      return result;
    } catch (err) {
      const msg = err.response?.data?.detail || errorMsg;
      setError(msg);
      addToast(msg, 'error');
      throw err;
    } finally {
      setLoading(false);
    }
  }, [addToast]);

  return { loading, error, execute };
}
