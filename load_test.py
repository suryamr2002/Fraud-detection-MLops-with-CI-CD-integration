#!/usr/bin/env python3
"""
Load Testing Script for Fraud Detection API
Tests auto-scaling capabilities under load

Usage:
    python load_test.py --url http://localhost:8000 --duration 300 --rate 50
"""

import argparse
import asyncio
import aiohttp
import time
import json
from datetime import datetime
from typing import List, Dict
import statistics

# Sample feature data (adjust based on your model's features)
SAMPLE_FEATURES = {
    "TransactionAmt": 100.0,
    "ProductCD": "W",
    "card1": 12345,
    "card2": 123,
    "card3": 150,
    "card4": "visa",
    "card5": 226,
    "card6": "credit",
    "addr1": 1,
    "addr2": 2,
    "dist1": 0.5,
    "dist2": 0.3,
    "P_emaildomain": "gmail.com",
    "R_emaildomain": "gmail.com",
    "C1": 1,
    "C2": 2,
    "C3": 3,
    "C4": 4,
    "C5": 5,
    "C6": 6,
    "C7": 7,
    "C8": 8,
    "C9": 9,
    "C10": 10,
    "C11": 11,
    "C12": 12,
    "C13": 13,
    "C14": 14,
    "D1": 0.1,
    "D2": 0.2,
    "D3": 0.3,
    "D4": 0.4,
    "D5": 0.5,
    "D6": 0.6,
    "D7": 0.7,
    "D8": 0.8,
    "D9": 0.9,
    "D10": 1.0,
    "D11": 1.1,
    "D12": 1.2,
    "D13": 1.3,
    "D14": 1.4,
    "D15": 1.5,
    "M1": "T",
    "M2": "T",
    "M3": "T",
    "M4": "T",
    "M5": "T",
    "M6": "T",
    "M7": "T",
    "M8": "T",
    "M9": "T",
    "V1": 1.0,
    "V2": 2.0,
    "V3": 3.0,
    "V4": 4.0,
    "V5": 5.0,
    "V6": 6.0,
    "V7": 7.0,
    "V8": 8.0,
    "V9": 9.0,
    "V10": 10.0,
    "V11": 11.0,
    "V12": 12.0,
    "V13": 13.0,
    "V14": 14.0,
    "V15": 15.0,
    "V16": 16.0,
    "V17": 17.0,
    "V18": 18.0,
    "V19": 19.0,
    "V20": 20.0,
    "V21": 21.0,
    "V22": 22.0,
    "V23": 23.0,
    "V24": 24.0,
    "V25": 25.0,
    "V26": 26.0,
    "V27": 27.0,
    "V28": 28.0,
    "V29": 29.0,
    "V30": 30.0,
    "V31": 31.0,
    "V32": 32.0,
    "V33": 33.0,
    "V34": 34.0,
    "V35": 35.0,
    "V36": 36.0,
    "V37": 37.0,
    "V38": 38.0,
    "V39": 39.0,
    "V40": 40.0,
    "V41": 41.0,
    "V42": 42.0,
    "V43": 43.0,
    "V44": 44.0,
    "V45": 45.0,
    "V46": 46.0,
    "V47": 47.0,
    "V48": 48.0,
    "V49": 49.0,
    "V50": 50.0,
    "V51": 51.0,
    "V52": 52.0,
    "V53": 53.0,
    "V54": 54.0,
    "V55": 55.0,
    "V56": 56.0,
    "V57": 57.0,
    "V58": 58.0,
    "V59": 59.0,
    "V60": 60.0,
    "V61": 61.0,
    "V62": 62.0,
    "V63": 63.0,
    "V64": 64.0,
    "V65": 65.0,
    "V66": 66.0,
    "V67": 67.0,
    "V68": 68.0,
    "V69": 69.0,
    "V70": 70.0,
    "V71": 71.0,
    "V72": 72.0,
    "V73": 73.0,
    "V74": 74.0,
    "V75": 75.0,
    "V76": 76.0,
    "V77": 77.0,
    "V78": 78.0,
    "V79": 79.0,
    "V80": 80.0,
    "V81": 81.0,
    "V82": 82.0,
    "V83": 83.0,
    "V84": 84.0,
    "V85": 85.0,
    "V86": 86.0,
    "V87": 87.0,
    "V88": 88.0,
    "V89": 89.0,
    "V90": 90.0,
    "V91": 91.0,
    "V92": 92.0,
    "V93": 93.0,
    "V94": 94.0,
    "V95": 95.0,
    "V96": 96.0,
    "V97": 97.0,
    "V98": 98.0,
    "V99": 99.0,
    "V100": 100.0,
    "V101": 101.0,
    "V102": 102.0,
    "V103": 103.0,
    "V104": 104.0,
    "V105": 105.0,
    "V106": 106.0,
    "V107": 107.0,
    "V108": 108.0,
    "V109": 109.0,
    "V110": 110.0,
    "V111": 111.0,
    "V112": 112.0,
    "V113": 113.0,
    "V114": 114.0,
    "V115": 115.0,
    "V116": 116.0,
    "V117": 117.0,
    "V118": 118.0,
    "V119": 119.0,
    "V120": 120.0,
    "V121": 121.0,
    "V122": 122.0,
    "V123": 123.0,
    "V124": 124.0,
    "V125": 125.0,
    "V126": 126.0,
    "V127": 127.0,
    "V128": 128.0,
    "V129": 129.0,
    "V130": 130.0,
    "V131": 131.0,
    "V132": 132.0,
    "V133": 133.0,
    "V134": 134.0,
    "V135": 135.0,
    "V136": 136.0,
    "V137": 137.0,
    "V138": 138.0,
    "V139": 139.0,
    "V140": 140.0,
    "V141": 141.0,
    "V142": 142.0,
    "V143": 143.0,
    "V144": 144.0,
    "V145": 145.0,
    "V146": 146.0,
    "V147": 147.0,
    "V148": 148.0,
    "V149": 149.0,
    "V150": 150.0,
    "V151": 151.0,
    "V152": 152.0,
    "V153": 153.0,
    "V154": 154.0,
    "V155": 155.0,
    "V156": 156.0,
    "V157": 157.0,
    "V158": 158.0,
    "V159": 159.0,
    "V160": 160.0,
    "V161": 161.0,
    "V162": 162.0,
    "V163": 163.0,
    "V164": 164.0,
    "V165": 165.0,
    "V166": 166.0,
    "V167": 167.0,
    "V168": 168.0,
    "V169": 169.0,
    "V170": 170.0,
    "V171": 171.0,
    "V172": 172.0,
    "V173": 173.0,
    "V174": 174.0,
    "V175": 175.0,
    "V176": 176.0,
    "V177": 177.0,
    "V178": 178.0,
    "V179": 179.0,
    "V180": 180.0,
    "V181": 181.0,
    "V182": 182.0,
    "V183": 183.0,
    "V184": 184.0,
    "V185": 185.0,
    "V186": 186.0,
    "V187": 187.0,
    "V188": 188.0,
    "V189": 189.0,
    "V190": 190.0,
    "V191": 191.0,
    "V192": 192.0,
    "V193": 193.0,
    "V194": 194.0,
    "V195": 195.0,
    "V196": 196.0,
    "V197": 197.0,
    "V198": 198.0,
    "V199": 199.0,
    "V200": 200.0,
    "V201": 201.0,
    "V202": 202.0,
    "V203": 203.0,
    "V204": 204.0,
    "V205": 205.0,
    "V206": 206.0,
    "V207": 207.0,
    "V208": 208.0,
    "V209": 209.0,
    "V210": 210.0,
    "V211": 211.0,
    "V212": 212.0,
    "V213": 213.0,
    "V214": 214.0,
    "V215": 215.0,
    "V216": 216.0,
    "V217": 217.0,
    "V218": 218.0,
    "V219": 219.0,
    "V220": 220.0,
    "V221": 221.0,
    "V222": 222.0,
    "V223": 223.0,
    "V224": 224.0,
    "V225": 225.0,
    "V226": 226.0,
    "V227": 227.0,
    "V228": 228.0,
    "V229": 229.0,
    "V230": 230.0,
    "V231": 231.0,
    "V232": 232.0,
    "V233": 233.0,
    "V234": 234.0,
    "V235": 235.0,
    "V236": 236.0,
    "V237": 237.0,
    "V238": 238.0,
    "V239": 239.0,
    "V240": 240.0,
    "V241": 241.0,
    "V242": 242.0,
    "V243": 243.0,
    "V244": 244.0,
    "V245": 245.0,
    "V246": 246.0,
    "V247": 247.0,
    "V248": 248.0,
    "V249": 249.0,
    "V250": 250.0,
    "V251": 251.0,
    "V252": 252.0,
    "V253": 253.0,
    "V254": 254.0,
    "V255": 255.0,
    "V256": 256.0,
    "V257": 257.0,
    "V258": 258.0,
    "V259": 259.0,
    "V260": 260.0,
    "V261": 261.0,
    "V262": 262.0,
    "V263": 263.0,
    "V264": 264.0,
    "V265": 265.0,
    "V266": 266.0,
    "V267": 267.0,
    "V268": 268.0,
    "V269": 269.0,
    "V270": 270.0,
    "V271": 271.0,
    "V272": 272.0,
    "V273": 273.0,
    "V274": 274.0,
    "V275": 275.0,
    "V276": 276.0,
    "V277": 277.0,
    "V278": 278.0,
    "V279": 279.0,
    "V280": 280.0,
    "V281": 281.0,
    "V282": 282.0,
    "V283": 283.0,
    "V284": 284.0,
    "V285": 285.0,
    "V286": 286.0,
    "V287": 287.0,
    "V288": 288.0,
    "V289": 289.0,
    "V290": 290.0,
    "V291": 291.0,
    "V292": 292.0,
    "V293": 293.0,
    "V294": 294.0,
    "V295": 295.0,
    "V296": 296.0,
    "V297": 297.0,
    "V298": 298.0,
    "V299": 299.0,
    "V300": 300.0,
    "V301": 301.0,
    "V302": 302.0,
    "V303": 303.0,
    "V304": 304.0,
    "V305": 305.0,
    "V306": 306.0,
    "V307": 307.0,
    "V308": 308.0,
    "V309": 309.0,
    "V310": 310.0,
    "V311": 311.0,
    "V312": 312.0,
    "V313": 313.0,
    "V314": 314.0,
    "V315": 315.0,
    "V316": 316.0,
    "V317": 317.0,
    "V318": 318.0,
    "V319": 319.0,
    "V320": 320.0,
    "V321": 321.0,
    "V322": 322.0,
    "V323": 323.0,
    "V324": 324.0,
    "V325": 325.0,
    "V326": 326.0,
    "V327": 327.0,
    "V328": 328.0,
    "V329": 329.0,
    "V330": 330.0,
    "V331": 331.0,
    "V332": 332.0,
    "V333": 333.0,
    "V334": 334.0,
    "V335": 335.0,
    "V336": 336.0,
    "V337": 337.0,
    "V338": 338.0,
    "V339": 339.0,
    "V340": 340.0,
}


class LoadTestStats:
    def __init__(self):
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.latencies: List[float] = []
        self.errors: List[str] = []
        self.start_time = None
        self.end_time = None

    def add_result(self, success: bool, latency: float, error: str = None):
        self.total_requests += 1
        if success:
            self.successful_requests += 1
            self.latencies.append(latency)
        else:
            self.failed_requests += 1
            if error:
                self.errors.append(error)

    def get_summary(self) -> Dict:
        if not self.latencies:
            return {
                "total_requests": self.total_requests,
                "successful": self.successful_requests,
                "failed": self.failed_requests,
                "success_rate": 0.0,
            }

        duration = (self.end_time - self.start_time).total_seconds() if self.end_time and self.start_time else 0
        rps = self.total_requests / duration if duration > 0 else 0

        return {
            "total_requests": self.total_requests,
            "successful": self.successful_requests,
            "failed": self.failed_requests,
            "success_rate": (self.successful_requests / self.total_requests) * 100,
            "requests_per_second": rps,
            "latency_p50": statistics.median(self.latencies),
            "latency_p95": self._percentile(self.latencies, 95),
            "latency_p99": self._percentile(self.latencies, 99),
            "latency_avg": statistics.mean(self.latencies),
            "latency_min": min(self.latencies),
            "latency_max": max(self.latencies),
            "duration_seconds": duration,
        }

    @staticmethod
    def _percentile(data: List[float], percentile: int) -> float:
        sorted_data = sorted(data)
        index = int(len(sorted_data) * percentile / 100)
        return sorted_data[min(index, len(sorted_data) - 1)]


async def make_request(session: aiohttp.ClientSession, url: str, payload: Dict) -> tuple:
    """Make a single prediction request"""
    start = time.time()
    try:
        async with session.post(f"{url}/predict", json=payload, timeout=aiohttp.ClientTimeout(total=30)) as response:
            latency = time.time() - start
            if response.status == 200:
                return True, latency, None
            else:
                error_text = await response.text()
                return False, latency, f"HTTP {response.status}: {error_text}"
    except asyncio.TimeoutError:
        return False, time.time() - start, "Timeout"
    except Exception as e:
        return False, time.time() - start, str(e)


async def worker(session: aiohttp.ClientSession, url: str, stats: LoadTestStats, rate: float, duration: float):
    """Worker coroutine that sends requests at specified rate"""
    interval = 1.0 / rate
    end_time = time.time() + duration
    request_id = 0

    while time.time() < end_time:
        request_start = time.time()
        
        # Vary features slightly for each request
        payload = {"data": {**SAMPLE_FEATURES}}
        payload["data"]["TransactionAmt"] = 50.0 + (request_id % 1000)
        
        success, latency, error = await make_request(session, url, payload)
        stats.add_result(success, latency, error)
        
        request_id += 1
        
        # Rate limiting
        elapsed = time.time() - request_start
        sleep_time = max(0, interval - elapsed)
        if sleep_time > 0:
            await asyncio.sleep(sleep_time)


async def run_load_test(url: str, duration: int, rate: int, concurrency: int):
    """Run the load test"""
    print(f"\n🚀 Starting Load Test")
    print(f"   URL: {url}")
    print(f"   Duration: {duration}s")
    print(f"   Target Rate: {rate} req/s")
    print(f"   Concurrency: {concurrency} workers")
    print(f"   Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    stats = LoadTestStats()
    stats.start_time = datetime.now()

    connector = aiohttp.TCPConnector(limit=concurrency * 2)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Health check first
        try:
            async with session.get(f"{url}/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status != 200:
                    print(f"❌ Health check failed: HTTP {response.status}")
                    return
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return

        print("✅ Health check passed\n")

        # Start workers
        workers_per_rate = max(1, concurrency // rate) if rate > 0 else concurrency
        tasks = []
        for i in range(concurrency):
            worker_rate = rate / concurrency
            task = asyncio.create_task(worker(session, url, stats, worker_rate, duration))
            tasks.append(task)

        # Wait for all workers
        await asyncio.gather(*tasks)

    stats.end_time = datetime.now()

    # Print results
    summary = stats.get_summary()
    print("\n" + "=" * 60)
    print("📊 LOAD TEST RESULTS")
    print("=" * 60)
    print(f"Total Requests:     {summary['total_requests']:,}")
    print(f"Successful:         {summary['successful']:,}")
    print(f"Failed:             {summary['failed']:,}")
    print(f"Success Rate:       {summary['success_rate']:.2f}%")
    print(f"Requests/sec:       {summary['requests_per_second']:.2f}")
    print(f"\nLatency Statistics:")
    print(f"  P50:              {summary['latency_p50']*1000:.2f} ms")
    print(f"  P95:              {summary['latency_p95']*1000:.2f} ms")
    print(f"  P99:              {summary['latency_p99']*1000:.2f} ms")
    print(f"  Average:          {summary['latency_avg']*1000:.2f} ms")
    print(f"  Min:               {summary['latency_min']*1000:.2f} ms")
    print(f"  Max:               {summary['latency_max']*1000:.2f} ms")
    print(f"\nDuration:           {summary['duration_seconds']:.2f}s")
    print("=" * 60)

    if stats.errors and len(stats.errors) <= 10:
        print("\n⚠️  Sample Errors:")
        for error in stats.errors[:10]:
            print(f"   - {error}")


def main():
    parser = argparse.ArgumentParser(description="Load test for Fraud Detection API")
    parser.add_argument("--url", default="http://localhost:8000", help="API URL")
    parser.add_argument("--duration", type=int, default=300, help="Test duration in seconds")
    parser.add_argument("--rate", type=int, default=50, help="Target requests per second")
    parser.add_argument("--concurrency", type=int, default=10, help="Number of concurrent workers")

    args = parser.parse_args()

    asyncio.run(run_load_test(args.url, args.duration, args.rate, args.concurrency))


if __name__ == "__main__":
    main()

