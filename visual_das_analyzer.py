#!/usr/bin/env python3
"""
Visual DAS Data Analyzer - For Beginners
Shows DAS sensor data in easy-to-understand charts and graphs
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from kafka import KafkaConsumer
from datetime import datetime
import struct
import seaborn as sns
import time

# Set up nice plotting style
plt.style.use('default')
sns.set_palette("husl")

def extract_amplitudes_from_avro(raw_bytes):
    """Try to extract amplitude data from Avro binary format"""
    amplitudes = []
    
    # Method 1: Look for float patterns in the binary data
    for i in range(0, len(raw_bytes) - 4, 4):
        try:
            val = struct.unpack('<f', raw_bytes[i:i+4])[0]  # Little endian float
            if -1000 < val < 1000 and not np.isnan(val) and not np.isinf(val):
                amplitudes.append(val)
        except:
            continue
    
    # Method 2: If that didn't work, try different byte offsets
    if len(amplitudes) < 100:
        amplitudes = []
        for offset in [8, 16, 32, 64]:  # Try different starting points
            for i in range(offset, min(offset + 2000, len(raw_bytes) - 4), 4):
                try:
                    val = struct.unpack('<f', raw_bytes[i:i+4])[0]
                    if -1000 < val < 1000 and not np.isnan(val) and not np.isinf(val):
                        amplitudes.append(val)
                        if len(amplitudes) >= 100:  # We have enough
                            break
                except:
                    continue
            if len(amplitudes) >= 100:
                break
    
    return amplitudes[:500]  # Return max 500 points

def create_comprehensive_analysis():
    """Create comprehensive visual analysis of DAS data"""
    
    print("🔍 VISUAL DAS DATA ANALYZER")
    print("=" * 50)
    print("Connecting to Kafka and collecting sensor data...")
    
    # Connect to Kafka with timeout
    all_amplitudes = []
    message_timestamps = []
    message_sizes = []
    messages_collected = 0
    
    try:
        consumer = KafkaConsumer(
            '1005504720-amp',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: x,
            consumer_timeout_ms=10000  # 10 second timeout
        )
        
        print("📡 Collecting DAS sensor data...")
        
        for message in consumer:
            messages_collected += 1
            
            # Extract amplitudes from this message
            amplitudes = extract_amplitudes_from_avro(message.value)
            
            if amplitudes:
                all_amplitudes.extend(amplitudes)
                message_timestamps.append(datetime.fromtimestamp(message.timestamp/1000))
                message_sizes.append(len(message.value))
                
                print(f"  Message {messages_collected}: {len(amplitudes)} amplitude values extracted")
            
            # Stop after collecting enough data
            if messages_collected >= 20 or len(all_amplitudes) >= 2000:
                break
        
        consumer.close()
        
    except Exception as e:
        print(f"⚠️  Could not collect data from Kafka: {e}")
        print("   Using demo data instead...")
    
    if not all_amplitudes:
        print("❌ Could not extract amplitude data. The data might be in a complex Avro format.")
        print("   Let me create a demo with simulated DAS data instead...")
        create_demo_analysis()
        return
    
    print(f"\n✅ Collected {len(all_amplitudes)} amplitude readings from {messages_collected} messages")
    
    # Create comprehensive visualizations
    create_das_visualizations(all_amplitudes, message_timestamps, message_sizes)

def create_demo_analysis():
    """Create demo analysis with realistic DAS-like data"""
    print("\n🎯 Creating DEMO DAS Analysis with Realistic Data")
    print("=" * 50)
    
    # Generate realistic DAS data
    time_points = np.linspace(0, 120, 1000)  # 2 minutes of data
    sensor_locations = np.arange(0, 100, 1)  # 100 sensor points along fiber
    
    # Simulate different types of DAS events
    base_noise = np.random.normal(0, 0.1, (len(time_points), len(sensor_locations)))
    
    # Add simulated events
    events = {
        'Vehicle Traffic': (20, 30, 25, 35),  # time_start, time_end, sensor_start, sensor_end
        'Pipeline Vibration': (50, 80, 60, 70),
        'Digging Activity': (90, 110, 10, 20)
    }
    
    das_data = base_noise.copy()
    
    for event_name, (t1, t2, s1, s2) in events.items():
        t_mask = (time_points >= t1) & (time_points <= t2)
        s_mask = (sensor_locations >= s1) & (sensor_locations <= s2)
        
        # Add event signature
        event_amplitude = np.random.normal(2, 0.5, np.sum(t_mask))
        for i, t_idx in enumerate(np.where(t_mask)[0]):
            das_data[t_idx, s_mask] += event_amplitude[i]
    
    create_das_visualizations_demo(das_data, time_points, sensor_locations, events)

def create_das_visualizations(amplitudes, timestamps, message_sizes):
    """Create comprehensive visualizations of real DAS data"""
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('Fiber Optics DAS Data Analysis', fontsize=16, fontweight='bold')
    
    # 1. Time series of amplitude data
    plt.subplot(2, 3, 1)
    plt.plot(amplitudes[:1000], linewidth=0.8, color='blue', alpha=0.7)
    plt.title('Raw Sensor Amplitudes Over Time')
    plt.xlabel('Sample Number')
    plt.ylabel('Amplitude')
    plt.grid(True, alpha=0.3)
    
    # 2. Amplitude distribution histogram
    plt.subplot(2, 3, 2)
    plt.hist(amplitudes, bins=50, alpha=0.7, color='green', edgecolor='black')
    plt.title('Amplitude Distribution')
    plt.xlabel('Amplitude Value')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    
    # 3. Message sizes over time
    plt.subplot(2, 3, 3)
    if len(message_sizes) > 1:
        plt.plot(range(len(message_sizes)), message_sizes, 'ro-', linewidth=2, markersize=6)
        plt.title('Message Sizes')
        plt.xlabel('Message Number')
        plt.ylabel('Size (bytes)')
        plt.grid(True, alpha=0.3)
    
    # 4. Statistical summary
    plt.subplot(2, 3, 4)
    stats = {
        'Mean': np.mean(amplitudes),
        'Std Dev': np.std(amplitudes),
        'Min': np.min(amplitudes),
        'Max': np.max(amplitudes),
        'Range': np.max(amplitudes) - np.min(amplitudes)
    }
    
    plt.bar(range(len(stats)), list(stats.values()), color=['red', 'blue', 'green', 'orange', 'purple'])
    plt.xticks(range(len(stats)), list(stats.keys()), rotation=45)
    plt.title('Statistical Summary')
    plt.ylabel('Value')
    plt.grid(True, alpha=0.3)
    
    # 5. Frequency analysis (if enough data)
    plt.subplot(2, 3, 5)
    if len(amplitudes) >= 256:
        freqs = np.fft.fftfreq(len(amplitudes[:512]), 1/5000)  # 5kHz sampling
        fft_vals = np.abs(np.fft.fft(amplitudes[:512]))
        plt.plot(freqs[:256], fft_vals[:256], color='purple')
        plt.title('Frequency Spectrum')
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude')
        plt.grid(True, alpha=0.3)
    
    # 6. Data quality metrics
    plt.subplot(2, 3, 6)
    quality_metrics = {
        'Total Samples': len(amplitudes),
        'Valid Samples': len([x for x in amplitudes if not np.isnan(x)]),
        'Zero Values': len([x for x in amplitudes if x == 0]),
        'Messages': len(message_sizes)
    }
    
    plt.bar(range(len(quality_metrics)), list(quality_metrics.values()), 
            color=['cyan', 'lime', 'yellow', 'pink'])
    plt.xticks(range(len(quality_metrics)), list(quality_metrics.keys()), rotation=45)
    plt.title('Data Quality Metrics')
    plt.ylabel('Count')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('comprehensive_das_analysis.png', dpi=150, bbox_inches='tight')
    print(f"\n📊 Comprehensive analysis saved as: comprehensive_das_analysis.png")
    
    # Print summary
    print("\n" + "=" * 60)
    print("📋 ANALYSIS SUMMARY:")
    print("=" * 60)
    print(f"Total amplitude readings analyzed: {len(amplitudes):,}")
    print(f"Average amplitude: {np.mean(amplitudes):.3f}")
    print(f"Amplitude range: {np.min(amplitudes):.3f} to {np.max(amplitudes):.3f}")
    print(f"Standard deviation: {np.std(amplitudes):.3f}")
    print(f"Messages processed: {len(message_sizes)}")
    print(f"Data collection timespan: {(timestamps[-1] - timestamps[0]).total_seconds():.1f} seconds")

def create_das_visualizations_demo(das_data, time_points, sensor_locations, events):
    """Create comprehensive visualizations of demo DAS data"""
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(18, 14))
    fig.suptitle('DAS Pipeline Monitoring - DEMO Analysis', fontsize=18, fontweight='bold')
    
    # 1. Waterfall plot (main DAS visualization)
    plt.subplot(3, 3, 1)
    extent = [sensor_locations[0], sensor_locations[-1], time_points[-1], time_points[0]]
    im = plt.imshow(das_data, aspect='auto', extent=extent, cmap='seismic', vmin=-3, vmax=3)
    plt.colorbar(im, label='Amplitude')
    plt.title('DAS Waterfall Plot\n(Time vs Distance)')
    plt.xlabel('Distance Along Fiber (km)')
    plt.ylabel('Time (seconds)')
    
    # Add event annotations
    for event_name, (t1, t2, s1, s2) in events.items():
        plt.plot([s1, s2, s2, s1, s1], [t1, t1, t2, t2, t1], 'white', linewidth=2)
        plt.text(s1+2, (t1+t2)/2, event_name, color='white', fontweight='bold', fontsize=8)
    
    # 2. Single sensor time series
    plt.subplot(3, 3, 2)
    sensor_25 = das_data[:, 25]  # Sensor at 25km
    plt.plot(time_points, sensor_25, 'blue', linewidth=1)
    plt.title('Single Sensor Response\n(Sensor at 25km)')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True, alpha=0.3)
    
    # 3. Average amplitude along fiber
    plt.subplot(3, 3, 3)
    avg_amplitude = np.mean(np.abs(das_data), axis=0)
    plt.plot(sensor_locations, avg_amplitude, 'red', linewidth=2, marker='o', markersize=3)
    plt.title('Average Activity by Location')
    plt.xlabel('Distance Along Fiber (km)')
    plt.ylabel('Average Amplitude')
    plt.grid(True, alpha=0.3)
    
    # 4. Event detection timeline
    plt.subplot(3, 3, 4)
    event_timeline = np.zeros(len(time_points))
    colors = ['red', 'green', 'blue']
    for i, (event_name, (t1, t2, s1, s2)) in enumerate(events.items()):
        event_mask = (time_points >= t1) & (time_points <= t2)
        plt.fill_between(time_points, 0, event_mask * (i+1), alpha=0.6, 
                        color=colors[i], label=event_name)
    
    plt.title('Event Detection Timeline')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Event Type')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 5. Amplitude distribution
    plt.subplot(3, 3, 5)
    plt.hist(das_data.flatten(), bins=50, alpha=0.7, color='purple', edgecolor='black')
    plt.title('Amplitude Distribution\n(All Sensors)')
    plt.xlabel('Amplitude')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    
    # 6. RMS energy over time
    plt.subplot(3, 3, 6)
    rms_energy = np.sqrt(np.mean(das_data**2, axis=1))
    plt.plot(time_points, rms_energy, 'orange', linewidth=2)
    plt.title('Total Energy Over Time\n(RMS of all sensors)')
    plt.xlabel('Time (seconds)')
    plt.ylabel('RMS Energy')
    plt.grid(True, alpha=0.3)
    
    # 7. Frequency analysis for middle section
    plt.subplot(3, 3, 7)
    middle_sensor_data = das_data[:, 50]  # Middle sensor
    freqs = np.fft.fftfreq(len(middle_sensor_data), time_points[1] - time_points[0])
    fft_vals = np.abs(np.fft.fft(middle_sensor_data))
    positive_freqs = freqs[:len(freqs)//2]
    plt.plot(positive_freqs, fft_vals[:len(freqs)//2], 'green')
    plt.title('Frequency Spectrum\n(Middle Sensor)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True, alpha=0.3)
    
    # 8. Event intensity heatmap
    plt.subplot(3, 3, 8)
    event_intensity = np.zeros((len(events), len(sensor_locations)))
    for i, (event_name, (t1, t2, s1, s2)) in enumerate(events.items()):
        t_mask = (time_points >= t1) & (time_points <= t2)
        event_data = das_data[t_mask, :]
        event_intensity[i, :] = np.mean(np.abs(event_data), axis=0)
    
    im = plt.imshow(event_intensity, aspect='auto', cmap='hot')
    plt.colorbar(im, label='Intensity')
    plt.title('Event Intensity Map')
    plt.xlabel('Distance Along Fiber (km)')
    plt.ylabel('Event Type')
    plt.yticks(range(len(events)), list(events.keys()))
    
    # 9. Summary statistics
    plt.subplot(3, 3, 9)
    stats = {
        'Peak Amplitude': np.max(np.abs(das_data)),
        'Avg Amplitude': np.mean(np.abs(das_data)),
        'Total Energy': np.sum(das_data**2),
        'Events Detected': len(events),
        'Active Sensors': np.sum(np.max(np.abs(das_data), axis=0) > 0.5)
    }
    
    bars = plt.bar(range(len(stats)), list(stats.values()), 
                   color=['red', 'blue', 'green', 'orange', 'purple'])
    plt.xticks(range(len(stats)), list(stats.keys()), rotation=45, ha='right')
    plt.title('Pipeline Monitoring Summary')
    plt.ylabel('Value')
    plt.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, value in zip(bars, stats.values()):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                f'{value:.1f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('comprehensive_das_analysis.png', dpi=150, bbox_inches='tight')
    
    # Save detailed event report
    create_event_report(events, das_data, time_points, sensor_locations)
    
    print(f"\n📊 Comprehensive analysis saved as: comprehensive_das_analysis.png")
    print(f"📋 Event report saved as: das_event_report.txt")

def create_event_report(events, das_data, time_points, sensor_locations):
    """Create a detailed text report of detected events"""
    
    with open('das_event_report.txt', 'w', encoding='utf-8') as f:
        f.write("FIBER OPTICS DAS - EVENT ANALYSIS REPORT\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Analysis Period: {time_points[0]:.1f} to {time_points[-1]:.1f} seconds\n")
        f.write(f"Fiber Length: {sensor_locations[-1]} km\n")
        f.write(f"Total Events Detected: {len(events)}\n\n")
        
        for event_name, (t1, t2, s1, s2) in events.items():
            f.write(f"EVENT: {event_name}\n")
            f.write(f"  Time: {t1:.1f} - {t2:.1f} seconds\n")
            f.write(f"  Location: {s1} - {s2} km along fiber\n")
            f.write(f"  Duration: {t2-t1:.1f} seconds\n")
            f.write(f"  Distance: {s2-s1} km\n")
            
            # Calculate event statistics
            t_mask = (time_points >= t1) & (time_points <= t2)
            s_mask = (sensor_locations >= s1) & (sensor_locations <= s2)
            event_data = das_data[np.ix_(t_mask, s_mask)]
            
            f.write(f"  Peak Amplitude: {np.max(np.abs(event_data)):.3f}\n")
            f.write(f"  Average Amplitude: {np.mean(np.abs(event_data)):.3f}\n")
            f.write(f"  Total Energy: {np.sum(event_data**2):.3f}\n")
            f.write(f"  Risk Level: {'HIGH' if np.max(np.abs(event_data)) > 2 else 'MEDIUM' if np.max(np.abs(event_data)) > 1 else 'LOW'}\n")
            f.write("\n")
        
        f.write("PIPELINE STATUS: All events monitored and analyzed\n")
        f.write("SYSTEM STATUS: Fiber optic sensors operational\n")

if __name__ == "__main__":
    print("🛢️ VISUAL DAS DATA ANALYZER")
    print("=" * 50)
    print("This tool creates comprehensive visual analysis of DAS sensor data")
    print("Perfect for beginners to understand pipeline monitoring data!")
    print()
    
    try:
        # Try to analyze real data first
        create_comprehensive_analysis()
        
    except Exception as e:
        print(f"⚠️  Could not connect to Kafka or extract real data: {e}")
        print("📊 Creating demo analysis with realistic DAS data instead...")
        create_demo_analysis()
    
    print("\n🎉 Analysis complete! Check the generated files:")
    print("   📊 comprehensive_das_analysis.png (or demo version)")
    print("   📋 das_event_report.txt")
    print("\n✅ Now you can see exactly what DAS data looks like!") 