#!/usr/bin/env python3
"""
DAS Results Viewer - Shows all your analysis results
"""

import os
import subprocess
import sys

def view_results():
    """Display all the generated analysis results"""
    
    print("🛢️ DAS ANALYSIS RESULTS VIEWER")
    print("=" * 50)
    
    # Check what files we have
    files = {
        'comprehensive_das_analysis.png': 'Real DAS data from your simulator',
        'complete_das_pipeline_analysis.png': 'Professional pipeline monitoring demo',
        'pipeline_monitoring_report.txt': 'Detailed technical report',
        'das_data_analysis.png': 'Basic data visualization'
    }
    
    available_files = []
    for filename, description in files.items():
        if os.path.exists(filename):
            available_files.append((filename, description))
            print(f"✅ {filename} - {description}")
        else:
            print(f"❌ {filename} - Not found")
    
    if not available_files:
        print("\n⚠️  No analysis files found. Run the analyzer first:")
        print("   python3 visual_das_analyzer.py")
        print("   python3 run_demo_analysis.py")
        return
    
    print(f"\n📊 Found {len(available_files)} analysis files")
    
    # Show what each file contains
    print("\n🔍 WHAT YOU CAN SEE IN EACH FILE:")
    print("=" * 40)
    
    if os.path.exists('comprehensive_das_analysis.png'):
        print("\n📈 comprehensive_das_analysis.png:")
        print("   • Raw sensor amplitude data over time")
        print("   • Amplitude distribution histogram")
        print("   • Message sizes and data quality metrics")
        print("   • Frequency spectrum analysis")
        print("   • Statistical summary of your real DAS data")
    
    if os.path.exists('complete_das_pipeline_analysis.png'):
        print("\n🌊 complete_das_pipeline_analysis.png:")
        print("   • MAIN VIEW: Waterfall plot (time vs distance)")
        print("   • Individual sensor responses")
        print("   • Event timeline showing:")
        print("     - Vehicle traffic (20-40s, 25-35km)")
        print("     - Equipment vibration (50-80s, 60-70km)")
        print("     - Unauthorized digging (90-110s, 10-20km)")
        print("     - Small leak detection (100-120s, 45-55km)")
        print("   • Risk assessment and energy profiles")
        print("   • Professional monitoring dashboard")
    
    if os.path.exists('pipeline_monitoring_report.txt'):
        print("\n📋 pipeline_monitoring_report.txt:")
        print("   • Executive summary of events")
        print("   • Detailed event analysis with risk levels")
        print("   • System performance metrics")
        print("   • Professional recommendations")
        print("   • Event interpretations (what each event means)")
    
    # Try to open files automatically
    print("\n🖼️  OPENING VISUALIZATIONS:")
    print("=" * 30)
    
    for filename, description in available_files:
        if filename.endswith('.png'):
            try:
                if sys.platform == "darwin":  # macOS
                    subprocess.run(['open', filename], check=True)
                    print(f"✅ Opened {filename} in default image viewer")
                elif sys.platform == "linux":
                    subprocess.run(['xdg-open', filename], check=True)
                    print(f"✅ Opened {filename} in default image viewer")
                elif sys.platform == "win32":
                    os.startfile(filename)
                    print(f"✅ Opened {filename} in default image viewer")
            except:
                print(f"⚠️  Could not auto-open {filename}. Open it manually.")
    
    # Show report content
    if os.path.exists('pipeline_monitoring_report.txt'):
        print(f"\n📖 PIPELINE MONITORING REPORT PREVIEW:")
        print("=" * 45)
        try:
            with open('pipeline_monitoring_report.txt', 'r') as f:
                # Show first 20 lines
                for i, line in enumerate(f):
                    if i >= 20:
                        print("   ... (see full report in pipeline_monitoring_report.txt)")
                        break
                    print(f"   {line.rstrip()}")
        except:
            print("   Could not read report file")
    
    print("\n🎓 UNDERSTANDING DAS DATA:")
    print("=" * 30)
    print("""
🔬 WHAT THE WATERFALL PLOT SHOWS:
   • X-axis: Distance along fiber optic cable (0-100 km)
   • Y-axis: Time (0-120 seconds)
   • Colors: Amplitude of vibrations detected
   • Red/Blue: Strong vibrations (events happening)
   • Green/White: Quiet background (normal operation)

🚨 EVENTS YOU CAN SEE:
   • Vehicle Traffic: Moving pattern across sensors
   • Digging: Strong localized vibrations
   • Equipment: Regular mechanical patterns
   • Leaks: Gradual amplitude increases

📊 REAL-WORLD MEANING:
   • This is exactly what engineers see monitoring pipelines
   • Each event would trigger alerts in real systems
   • Engineers analyze these patterns to protect infrastructure
   • Your simulator generated the same data format as real DAS
    """)
    
    print("\n✅ CONGRATULATIONS!")
    print("=" * 20)
    print("You now understand fiber optic pipeline monitoring!")
    print("These visualizations show the same type of data pipeline engineers")
    print("use to protect oil & gas infrastructure 24/7.")

if __name__ == "__main__":
    view_results() 