import { useEffect, useState } from "react";

export interface User {
  username: string;
  id: number;
  is_active: boolean;
  authDisabled: boolean;
}

export const mockUser: User = {
  username: "admin@yacht.local",
  id: 0,
  is_active: true,
  authDisabled: true,
};

export const useFetch = (url: string) => {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!url) return;

    const fetchData = async () => {
      try {
        const response = await fetch(url);
        const data = await response.json();
        setData(data);
        setLoading(false);
      } catch (error) {
        setError(`Error fetching: ${error}`);
      }
    };

    fetchData();
  }, [url]);
  return { data, error, loading };
};
