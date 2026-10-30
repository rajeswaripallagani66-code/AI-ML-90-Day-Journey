import http from 'k6/http';
import { sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 10 },
    { duration: '1m', target: 50 },
    { duration: '30s', target: 0 },
  ],
};

export default function () {
  http.post('http://localhost:8000/predict', JSON.stringify({data: [0.1,0.2,0.3]}), {
    headers: { 'Content-Type': 'application/json' },
  });
  sleep(1);
}