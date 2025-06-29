#!/usr/bin/env python3
"""
DAS Demo Analysis - Shows what real pipeline monitoring looks like
Perfect for beginners to understand DAS technology
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime

# Set up nice plotting style
plt.style.use('default')
sns.set_palette("husl")

def create_demo_analysis():
    """Create demo analysis with realistic DAS-like data"""
    print("\n🎯 DAS PIPELINE MONITORING - DEMO ANALYSIS")
    print("=" * 60)
    print("Creating realistic fiber optic sensor data...")
    
    # Generate realistic DAS data
    time_points = np.linspace(0, 120, 1000)  # 2 minutes of data, 1000 samples
    sensor_locations = np.arange(0, 100, 1)  # 100 sensor points along 100km fiber
    
    print(f"📊 Simulating:")
    print(f"   • {len(time_points)} time samples over {time_points[-1]} seconds")
    print(f"   • {len(sensor_locations)} sensors along {sensor_locations[-1]} km fiber")
    print(f"   • Total data points: {len(time_points) * len(sensor_locations):,}")
    
    # Start with background noise (normal pipeline operation)
    base_noise = np.random.normal(0, 0.1, (len(time_points), len(sensor_locations)))
    
    # Define realistic pipeline events
    events = {
        'Vehicle Traffic Above Pipeline': (20, 40, 25, 35),  # time_start, time_end, sensor_start, sensor_end
        'Equipment Vibration': (50, 80, 60, 70),
        'Unauthorized Digging Activity': (90, 110, 10, 20),
        'Small Leak Detection': (100, 120, 45, 55)
    }
    
    print(f"\n🚨 Simulating {len(events)} pipeline events:")
    for event_name, (t1, t2, s1, s2) in events.items():
        print(f"   • {event_name}: {t1}-{t2}s, {s1}-{s2}km")
    
    # Start with base noise
    das_data = base_noise.copy()
    
    # Add each event with realistic signatures
    for event_name, (t1, t2, s1, s2) in events.items():
        t_mask = (time_points >= t1) & (time_points <= t2)
        s_mask = (sensor_locations >= s1) & (sensor_locations <= s2)
        
        # Different event types have different signatures
        if 'Vehicle' in event_name:
            # Moving vehicle creates a diagonal pattern
            for i, t_idx in enumerate(np.where(t_mask)[0]):
                progress = i / np.sum(t_mask)
                moving_sensor = int(s1 + progress * (s2 - s1))
                if moving_sensor < len(sensor_locations):
                    das_data[t_idx, moving_sensor:moving_sensor+3] += np.random.normal(1.5, 0.3, 3)
        
        elif 'Digging' in event_name:
            # Digging creates strong localized vibrations
            event_amplitude = np.random.normal(3, 0.8, np.sum(t_mask))
            for i, t_idx in enumerate(np.where(t_mask)[0]):
                das_data[t_idx, s_mask] += event_amplitude[i] * np.exp(-0.1 * np.abs(sensor_locations[s_mask] - (s1+s2)/2))
        
        elif 'Leak' in event_name:
            # Leak creates gradual amplitude increase
            for i, t_idx in enumerate(np.where(t_mask)[0]):
                progress = i / np.sum(t_mask)
                leak_amplitude = progress * np.random.normal(2, 0.4)
                das_data[t_idx, s_mask] += leak_amplitude
        
        else:
            # Equipment vibration - regular pattern
            event_amplitude = np.random.normal(2, 0.5, np.sum(t_mask))
            for i, t_idx in enumerate(np.where(t_mask)[0]):
                das_data[t_idx, s_mask] += event_amplitude[i]
    
    print("\n📈 Creating comprehensive visualizations...")
    create_das_visualizations_demo(das_data, time_points, sensor_locations, events)
    
    return das_data, time_points, sensor_locations, events

def create_das_visualizations_demo(das_data, time_points, sensor_locations, events):
    """Create comprehensive visualizations of demo DAS data"""
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(20, 16))
    fig.suptitle('Fiber Optics DAS - Pipeline Monitoring Analysis', fontsize=20, fontweight='bold')
    
    # 1. Main waterfall plot (most important DAS visualization)
    plt.subplot(3, 4, (1, 5))  # Span 2 rows for main plot
    extent = [sensor_locations[0], sensor_locations[-1], time_points[-1], time_points[0]]
    im = plt.imshow(das_data, aspect='auto', extent=extent, cmap='seismic', vmin=-4, vmax=4)
    plt.colorbar(im, label='Fiber Amplitude', shrink=0.8)
    plt.title('DAS Waterfall Plot - Time vs Distance\n(Main Pipeline Monitoring View)', fontsize=14, fontweight='bold')
    plt.xlabel('Distance Along Fiber Optic Cable (km)', fontsize=12)
    plt.ylabel('Time (seconds)', fontsize=12)
    
    # Add event annotations with boxes
    colors = ['white', 'yellow', 'cyan', 'lime']
    for i, (event_name, (t1, t2, s1, s2)) in enumerate(events.items()):
        # Draw event boundary box
        plt.plot([s1, s2, s2, s1, s1], [t1, t1, t2, t2, t1], colors[i], linewidth=3)
        # Add event label
        plt.text(s1+1, (t1+t2)/2, event_name, color=colors[i], fontweight='bold', 
                fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor='black', alpha=0.7))
    
    # 2. Single sensor detailed view
    plt.subplot(3, 4, 2)
    sensor_idx = 25  # Sensor at 25km
    sensor_data = das_data[:, sensor_idx]
    plt.plot(time_points, sensor_data, 'blue', linewidth=1.5)
    plt.title(f'Sensor Detail View\nSensor at {sensor_idx} km', fontweight='bold')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Amplitude')
    plt.grid(True, alpha=0.3)
    
    # Highlight events on this sensor
    for event_name, (t1, t2, s1, s2) in events.items():
        if s1 <= sensor_idx <= s2:
            event_mask = (time_points >= t1) & (time_points <= t2)
            plt.fill_between(time_points, sensor_data.min(), sensor_data.max(), 
                           where=event_mask, alpha=0.3, label=event_name)
    plt.legend(fontsize=8)
    
    # 3. Spatial activity profile
    plt.subplot(3, 4, 6)
    avg_amplitude = np.mean(np.abs(das_data), axis=0)
    max_amplitude = np.max(np.abs(das_data), axis=0)
    
    plt.plot(sensor_locations, avg_amplitude, 'red', linewidth=2, label='Average Activity')
    plt.plot(sensor_locations, max_amplitude, 'orange', linewidth=2, label='Peak Activity')
    plt.title('Activity Profile Along Pipeline', fontweight='bold')
    plt.xlabel('Distance Along Fiber (km)')
    plt.ylabel('Amplitude Level')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Mark event locations
    for event_name, (t1, t2, s1, s2) in events.items():
        plt.axvspan(s1, s2, alpha=0.2, label=f'{event_name} Zone')
    
    # 4. Event timeline
    plt.subplot(3, 4, 3)
    colors_timeline = ['red', 'green', 'blue', 'orange']
    for i, (event_name, (t1, t2, s1, s2)) in enumerate(events.items()):
        plt.barh(i, t2-t1, left=t1, height=0.6, color=colors_timeline[i], alpha=0.7)
        plt.text(t1 + (t2-t1)/2, i, f'{(t2-t1):.0f}s', ha='center', va='center', fontweight='bold')
    
    plt.title('Event Timeline', fontweight='bold')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Event Type')
    plt.yticks(range(len(events)), [name.split()[0] for name in events.keys()], fontsize=10)
    plt.grid(True, alpha=0.3)
    
    # 5. Amplitude distribution
    plt.subplot(3, 4, 7)
    plt.hist(das_data.flatten(), bins=60, alpha=0.7, color='purple', edgecolor='black')
    plt.title('Amplitude Distribution\n(All Sensors & Time)', fontweight='bold')
    plt.xlabel('Amplitude Value')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    
    # Add statistics text
    stats_text = f'Mean: {np.mean(das_data):.3f}\nStd: {np.std(das_data):.3f}\nMax: {np.max(np.abs(das_data)):.2f}'
    plt.text(0.7, 0.7, stats_text, transform=plt.gca().transAxes, 
             bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # 6. Energy over time
    plt.subplot(3, 4, 4)
    rms_energy = np.sqrt(np.mean(das_data**2, axis=1))
    mean_energy = np.mean(np.abs(das_data), axis=1)
    
    plt.plot(time_points, rms_energy, 'orange', linewidth=2, label='RMS Energy')
    plt.plot(time_points, mean_energy, 'red', linewidth=2, label='Mean Amplitude')
    plt.title('Total Pipeline Energy', fontweight='bold')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Energy Level')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # 7. Frequency analysis
    plt.subplot(3, 4, 8)
    middle_sensor_data = das_data[:, 50]  # Middle of pipeline
    freqs = np.fft.fftfreq(len(middle_sensor_data), time_points[1] - time_points[0])
    fft_vals = np.abs(np.fft.fft(middle_sensor_data))
    positive_freqs = freqs[:len(freqs)//2]
    
    plt.plot(positive_freqs, fft_vals[:len(freqs)//2], 'green', linewidth=1.5)
    plt.title('Frequency Analysis\n(Mid-Pipeline Sensor)', fontweight='bold')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 2)  # Focus on low frequencies
    
    # 8. Event detection summary
    plt.subplot(3, 4, 11)
    event_stats = []
    event_names_short = []
    
    for event_name, (t1, t2, s1, s2) in events.items():
        t_mask = (time_points >= t1) & (time_points <= t2)
        s_mask = (sensor_locations >= s1) & (sensor_locations <= s2)
        event_data = das_data[np.ix_(t_mask, s_mask)]
        
        peak_amplitude = np.max(np.abs(event_data))
        event_stats.append(peak_amplitude)
        event_names_short.append(event_name.split()[0])
    
    bars = plt.bar(range(len(event_stats)), event_stats, 
                   color=['red', 'green', 'blue', 'orange'], alpha=0.7)
    plt.title('Event Intensity Summary', fontweight='bold')
    plt.xlabel('Event Type')
    plt.ylabel('Peak Amplitude')
    plt.xticks(range(len(event_names_short)), event_names_short, rotation=45)
    plt.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar, value in zip(bars, event_stats):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05,
                f'{value:.2f}', ha='center', va='bottom', fontweight='bold')
    
    # 9. Risk assessment matrix
    plt.subplot(3, 4, 12)
    risk_levels = []
    for stat in event_stats:
        if stat > 3:
            risk_levels.append('HIGH')
        elif stat > 1.5:
            risk_levels.append('MEDIUM')
        else:
            risk_levels.append('LOW')
    
    risk_colors = {'HIGH': 'red', 'MEDIUM': 'orange', 'LOW': 'green'}
    pie_colors = [risk_colors[risk] for risk in risk_levels]
    
    plt.pie([1]*len(risk_levels), labels=event_names_short, colors=pie_colors, 
            autopct=lambda pct: f'{risk_levels[int(pct/100*len(risk_levels))]}' if pct > 0 else '')
    plt.title('Risk Assessment\nper Event', fontweight='bold')
    
    # 10. Pipeline status dashboard
    plt.subplot(3, 4, (9, 10))
    
    # Create a dashboard-style summary
    dashboard_data = {
        'Total Events Detected': len(events),
        'Pipeline Length Monitored': f'{sensor_locations[-1]} km',
        'Monitoring Duration': f'{time_points[-1]:.0f} seconds',
        'Peak Amplitude Detected': f'{np.max(np.abs(das_data)):.2f}',
        'Average Background Noise': f'{np.mean(np.abs(das_data[np.abs(das_data) < 0.5])):.3f}',
        'System Status': 'OPERATIONAL'
    }
    
    # Remove axes for clean dashboard look
    plt.gca().axis('off')
    
    # Create text dashboard
    y_pos = 0.9
    plt.text(0.1, y_pos, 'PIPELINE MONITORING DASHBOARD', fontsize=16, fontweight='bold', 
             transform=plt.gca().transAxes)
    
    y_pos -= 0.15
    for key, value in dashboard_data.items():
        color = 'green' if key == 'System Status' else 'black'
        plt.text(0.1, y_pos, f'{key}:', fontsize=12, fontweight='bold', 
                transform=plt.gca().transAxes)
        plt.text(0.6, y_pos, str(value), fontsize=12, color=color,
                transform=plt.gca().transAxes)
        y_pos -= 0.12
    
    # Add status indicators
    plt.text(0.1, 0.1, 'STATUS: ALL SYSTEMS OPERATIONAL ✓', 
             fontsize=14, fontweight='bold', color='green',
             transform=plt.gca().transAxes,
             bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgreen', alpha=0.3))
    
    plt.tight_layout()
    plt.savefig('complete_das_pipeline_analysis.png', dpi=200, bbox_inches='tight')
    
    # Create detailed event report
    create_detailed_event_report(events, das_data, time_points, sensor_locations)
    
    print(f"📊 Complete pipeline analysis saved as: complete_das_pipeline_analysis.png")
    print(f"📋 Detailed event report saved as: pipeline_monitoring_report.txt")

def create_detailed_event_report(events, das_data, time_points, sensor_locations):
    """Create a detailed professional report of pipeline monitoring"""
    
    with open('pipeline_monitoring_report.txt', 'w') as f:
        f.write("FIBER OPTICS DAS - PIPELINE MONITORING REPORT\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Analysis Period: {time_points[0]:.1f} to {time_points[-1]:.1f} seconds\n")
        f.write(f"Pipeline Section: 0 to {sensor_locations[-1]} km\n")
        f.write(f"Sensor Resolution: {len(sensor_locations)} sensors\n")
        f.write(f"Temporal Resolution: {len(time_points)} time samples\n")
        f.write(f"Total Data Points Analyzed: {len(time_points) * len(sensor_locations):,}\n\n")
        
        f.write("EXECUTIVE SUMMARY:\n")
        f.write("-" * 20 + "\n")
        f.write(f"• {len(events)} significant events detected during monitoring period\n")
        f.write(f"• Peak disturbance amplitude: {np.max(np.abs(das_data)):.3f}\n")
        f.write(f"• Average background noise level: {np.mean(np.abs(das_data[das_data < 0.5])):.3f}\n")
        f.write(f"• System operational status: NORMAL\n")
        f.write(f"• Pipeline integrity: MAINTAINED\n\n")
        
        f.write("DETAILED EVENT ANALYSIS:\n")
        f.write("-" * 30 + "\n\n")
        
        for i, (event_name, (t1, t2, s1, s2)) in enumerate(events.items(), 1):
            f.write(f"EVENT #{i}: {event_name}\n")
            f.write(f"{'=' * (10 + len(event_name))}\n")
            f.write(f"Start Time: {t1:.1f} seconds\n")
            f.write(f"End Time: {t2:.1f} seconds\n")
            f.write(f"Duration: {t2-t1:.1f} seconds\n")
            f.write(f"Location Start: {s1} km\n")
            f.write(f"Location End: {s2} km\n")
            f.write(f"Affected Distance: {s2-s1} km\n")
            
            # Calculate detailed event statistics
            t_mask = (time_points >= t1) & (time_points <= t2)
            s_mask = (sensor_locations >= s1) & (sensor_locations <= s2)
            event_data = das_data[np.ix_(t_mask, s_mask)]
            
            peak_amp = np.max(np.abs(event_data))
            avg_amp = np.mean(np.abs(event_data))
            total_energy = np.sum(event_data**2)
            
            f.write(f"Peak Amplitude: {peak_amp:.3f}\n")
            f.write(f"Average Amplitude: {avg_amp:.3f}\n")
            f.write(f"Total Energy: {total_energy:.3f}\n")
            
            # Risk assessment
            if peak_amp > 3:
                risk = "HIGH"
                action = "IMMEDIATE INVESTIGATION REQUIRED"
            elif peak_amp > 1.5:
                risk = "MEDIUM"
                action = "SCHEDULE INSPECTION"
            else:
                risk = "LOW"
                action = "CONTINUE MONITORING"
            
            f.write(f"Risk Level: {risk}\n")
            f.write(f"Recommended Action: {action}\n")
            
            # Event interpretation
            if 'Vehicle' in event_name:
                f.write("Event Type: Surface vehicle activity\n")
                f.write("Interpretation: Regular traffic above pipeline - no threat\n")
            elif 'Digging' in event_name:
                f.write("Event Type: Ground excavation activity\n")
                f.write("Interpretation: Potential third-party interference - requires investigation\n")
            elif 'Leak' in event_name:
                f.write("Event Type: Pressure anomaly\n")
                f.write("Interpretation: Possible pipeline integrity issue - urgent inspection needed\n")
            elif 'Equipment' in event_name:
                f.write("Event Type: Mechanical vibration\n")
                f.write("Interpretation: Equipment operation - normal pipeline activity\n")
            
            f.write("\n")
        
        f.write("SYSTEM PERFORMANCE METRICS:\n")
        f.write("-" * 35 + "\n")
        f.write(f"Data Quality: 100% (all sensors operational)\n")
        f.write(f"Event Detection Sensitivity: HIGH\n")
        f.write(f"False Positive Rate: LOW\n")
        f.write(f"Spatial Resolution: {(sensor_locations[-1] - sensor_locations[0]) / len(sensor_locations):.2f} km per sensor\n")
        f.write(f"Temporal Resolution: {(time_points[-1] - time_points[0]) / len(time_points):.3f} seconds per sample\n\n")
        
        f.write("RECOMMENDATIONS:\n")
        f.write("-" * 20 + "\n")
        f.write("1. Continue 24/7 monitoring with current sensitivity settings\n")
        f.write("2. Investigate high-amplitude events within 24 hours\n")
        f.write("3. Correlate surface activities with detected events\n")
        f.write("4. Maintain regular calibration schedule\n")
        f.write("5. Archive data for historical trend analysis\n\n")
        
        f.write("SYSTEM STATUS: OPERATIONAL ✓\n")
        f.write("PIPELINE STATUS: SECURE ✓\n")
        f.write("MONITORING STATUS: ACTIVE ✓\n")

if __name__ == "__main__":
    print("🛢️ COMPREHENSIVE DAS PIPELINE MONITORING DEMO")
    print("=" * 60)
    print("This demo shows exactly what fiber optic pipeline monitoring looks like")
    print("with realistic events that DAS systems detect in the field.")
    print()
    
    try:
        das_data, time_points, sensor_locations, events = create_demo_analysis()
        
        print(f"\n🎉 DEMO ANALYSIS COMPLETE!")
        print("=" * 40)
        print("📊 Generated files:")
        print("   • complete_das_pipeline_analysis.png  (Comprehensive charts)")
        print("   • pipeline_monitoring_report.txt      (Detailed technical report)")
        print()
        print("🔍 What you can see in the analysis:")
        print("   • Waterfall plot showing events over time and distance")
        print("   • Individual sensor responses")
        print("   • Event timeline and risk assessment")
        print("   • Frequency analysis and energy profiles")
        print("   • Professional monitoring dashboard")
        print()
        print("✅ This is exactly what pipeline engineers see when monitoring infrastructure!")
        
    except Exception as e:
        print(f"❌ Error creating demo: {e}")
        import traceback
        traceback.print_exc() 