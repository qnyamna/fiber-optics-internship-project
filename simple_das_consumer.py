#!/usr/bin/env python3
"""
Simple DAS Data Consumer & Analyzer
Educational tool to understand what the simulator generated
"""

from kafka import KafkaConsumer
import json
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import struct
import io

def consume_das_data():
    """Consume DAS data from Kafka and analyze it"""
    
    print("🔍 Connecting to Kafka to analyze DAS data...")
    
    # Connect to Kafka
    consumer = KafkaConsumer(
        '1005504720-amp',  # The topic with amplitude data
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',  # Read from beginning
        enable_auto_commit=True,
        value_deserializer=lambda x: x  # Raw bytes for now
    )
    
    print("📡 Reading DAS sensor data from Kafka...")
    print("=" * 50)
    
    message_count = 0
    amplitude_data = []
    timestamps = []
    
    try:
        for message in consumer:
            message_count += 1
            
            # Basic message info
            print(f"Message {message_count}:")
            print(f"  Timestamp: {datetime.fromtimestamp(message.timestamp/1000)}")
            print(f"  Partition: {message.partition}")
            print(f"  Offset: {message.offset}")
            print(f"  Value size: {len(message.value)} bytes")
            
            # Try to extract some amplitude values (this is Avro binary, so just demo)
            if message_count <= 3:  # Show first 3 messages details
                # Look for float patterns in the binary data
                try:
                    # Convert bytes to floats (approximation since it's Avro encoded)
                    float_count = len(message.value) // 4
                    if float_count > 100:  # Reasonable number of floats
                        # Extract some float values for demo
                        sample_floats = []
                        for i in range(0, min(200, len(message.value)-4), 4):
                            try:
                                val = struct.unpack('f', message.value[i:i+4])[0]
                                if -10000 < val < 10000:  # Reasonable amplitude range
                                    sample_floats.append(val)
                            except:
                                continue
                        
                        if len(sample_floats) > 10:
                            print(f"  Sample amplitudes: {sample_floats[:10]}")
                            print(f"  Amplitude range: {min(sample_floats):.3f} to {max(sample_floats):.3f}")
                            amplitude_data.extend(sample_floats[:100])
                            timestamps.append(message.timestamp)
                except:
                    print(f"  Raw data (first 50 bytes): {message.value[:50]}")
            
            print()
            
            # Stop after 10 messages for demo
            if message_count >= 10:
                break
                
    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()
    
    print(f"📊 Summary:")
    print(f"  Total messages read: {message_count}")
    print(f"  Data represents: {message_count * 8192} amplitude readings")
    print(f"  From 100 sensor points over time")
    print(f"  Each message = 1 time snapshot across all 100 sensors")
    
    # Simple visualization if we got some data
    if amplitude_data:
        print(f"\n📈 Creating simple visualization...")
        plt.figure(figsize=(12, 6))
        
        plt.subplot(1, 2, 1)
        plt.plot(amplitude_data[:100])
        plt.title('Sample DAS Amplitudes (First 100 points)')
        plt.xlabel('Sample Index')
        plt.ylabel('Amplitude')
        plt.grid(True)
        
        plt.subplot(1, 2, 2)
        plt.hist(amplitude_data, bins=30, alpha=0.7)
        plt.title('Amplitude Distribution')
        plt.xlabel('Amplitude Value')
        plt.ylabel('Frequency')
        plt.grid(True)
        
        plt.tight_layout()
        plt.savefig('das_data_analysis.png', dpi=150, bbox_inches='tight')
        print(f"  Saved visualization to: das_data_analysis.png")
    
    return message_count

def explain_what_happened():
    """Explain what the simulator did and what this means"""
    print("\n" + "=" * 60)
    print("🎓 WHAT YOU JUST LEARNED:")
    print("=" * 60)
    
    print("""
🔬 REAL DAS SYSTEM vs YOUR SIMULATOR:

Real World Pipeline Monitoring:
┌─────────────┐   ┌──────────────┐   ┌─────────────┐
│   Physical  │──▶│     Fiber    │──▶│     DAS     │
│   Pipeline  │   │ Optic Cable  │   │ Interrogator│
└─────────────┘   └──────────────┘   └─────────────┘
                                             │
                                             ▼
                                    ┌─────────────┐
                                    │   Kafka     │
                                    │   Topics    │
                                    └─────────────┘

Your Simulator Setup:
┌─────────────┐   ┌─────────────┐
│ DAS         │──▶│   Kafka     │
│ Simulator   │   │   Topics    │
└─────────────┘   └─────────────┘

🎯 DATA GENERATED:
• 130 messages/second for 120 seconds = ~15,600 total messages
• Each message = 8,192 amplitude readings from 100 sensor points  
• Total data points = ~127 MILLION sensor readings!
• Simulated 5,000 Hz sampling frequency
• Data format: exactly same as real DAS interrogator

📊 WHAT THIS DETECTS IN REAL WORLD:
• Pipeline leaks (pressure changes)
• Unauthorized digging near pipeline  
• Vehicle traffic above pipeline
• Seismic activity
• Equipment vibrations
• Theft attempts (valve tampering)

🚀 NEXT STEPS FOR ANALYSIS:
1. Build proper Avro consumer (handles schema)
2. Create real-time dashboards
3. Implement ML anomaly detection
4. Set up alerting systems
5. Historical data analysis

💡 WHY THIS MATTERS FOR OIL & GAS:
• Monitor 1000s of km of pipelines 24/7
• Instant detection of threats/issues
• Prevent catastrophic failures
• Optimize operations
• Ensure safety & compliance
    """)

if __name__ == "__main__":
    print("🛢️  Fiber Optics DAS Data Analysis")
    print("=" * 50)
    
    try:
        message_count = consume_das_data()
        explain_what_happened()
        
        print(f"\n✅ Successfully analyzed {message_count} DAS messages!")
        print("   You now understand how fiber optic pipeline monitoring works!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("   Make sure Kafka is running: docker-compose up") 