import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
};

export default function () {
  const url = `${__ENV.URL}/`;
  http.get(url);
  sleep(1);
  
  const payload = JSON.stringify({
    rms: 0.5,
    peak: 1.2,
    crest_factor: 2.4,
    kurtosis: 3.1,
    skewness: 0.2,
    mean: 0.01,
    std: 0.5,
    peak_to_peak: 2.4,
    impulse_factor: 2.5,
    clearance_factor: 2.3,
    shape_factor: 1.1
  });
  
  const params = { headers: { 'Content-Type': 'application/json' } };
  http.post(`${__ENV.URL}/predict`, payload, params);
  sleep(1);
}