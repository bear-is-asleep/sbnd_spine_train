#!/usr/bin/env python3

import re
import os
import sys
from collections import defaultdict, Counter
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def parse_fd_log(log_file):
    """Parse the file descriptor log and extract package information."""
    packages = defaultdict(set)
    fullpaths = defaultdict(set)
    fullpaths_all = defaultdict(list) #store as list to keep duplicates
    total_count = 0
    root_count = 0
    
    with open(log_file, 'r') as f:
        for line in f:
            # Skip lines that don't contain file descriptors
            if not line.strip().startswith('lr-x------ 1 bearc users 64 Mar 12 19:16'):
                continue
                
            total_count += 1
            
            # Extract the path from the line
            match = re.search(r'-> (.*?)$', line.strip())
            if not match:
                continue
                
            path = match.group(1)
            
            # Extract package information
            if 'dist-packages' in path:
                # Python packages
                parts = path.split('dist-packages/')
                if len(parts) > 1:
                    package_path = parts[1].split('/')
                    if len(package_path) > 0:
                        main_package = package_path[0]
                        packages["python"].add(main_package)
                        fullpaths[main_package].add(path)
                        fullpaths_all[main_package].append(path)
            elif 'lib-dynload' in path:
                # Python built-in modules
                packages["python_builtin"].add(os.path.basename(path))
                fullpaths["python_builtin"].add(path)
                fullpaths_all["python_builtin"].append(path)
            elif '/root/lib/' in path or '.pcm' in path:
                # All ROOT files
                packages["root"].add(os.path.basename(path))
                root_count += 1
                fullpaths["root"].add(path)
                fullpaths_all["root"].append(path)
            elif 'nvidia/' in path:
                # All NVIDIA components
                packages["nvidia"].add(os.path.basename(path))
                fullpaths["nvidia"].add(path)
                fullpaths_all["nvidia"].append(path)
            elif 'torch/' in path:
                # All PyTorch components
                packages["pytorch"].add(os.path.basename(path))
                fullpaths["pytorch"].add(path)
                fullpaths_all["pytorch"].append(path)
            elif '/lib/' in path and path.endswith('.so'):
                # All shared libraries
                packages["shared_libs"].add(os.path.basename(path))
                fullpaths["shared_libs"].add(path)
                fullpaths_all["shared_libs"].append(path)
            elif '/lib/x86_64-linux-gnu/' in path:
                # System libraries
                packages["system_libs"].add(os.path.basename(path))
                fullpaths["system_libs"].add(path)
                fullpaths_all["system_libs"].append(path)
            elif '/bin/' in path:
                # Executables
                packages["executables"].add(os.path.basename(path))
                fullpaths["executables"].add(path)
                fullpaths_all["executables"].append(path)
            elif 'scipy' in path:
                packages["scipy"].add(os.path.basename(path))
                fullpaths["scipy"].add(path)
                fullpaths_all["scipy"].append(path)
            elif 'numpy' in path:
                packages["numpy"].add(os.path.basename(path))
                fullpaths["numpy"].add(path)
                fullpaths_all["numpy"].append(path)
            elif 'matplotlib' in path:
                packages["matplotlib"].add(os.path.basename(path))
                fullpaths["matplotlib"].add(path)
                fullpaths_all["matplotlib"].append(path)
            elif 'pandas' in path:
                packages["pandas"].add(os.path.basename(path))
                fullpaths["pandas"].add(path)
                fullpaths_all["pandas"].append(path)
            elif 'sklearn' in path:
                packages["sklearn"].add(os.path.basename(path))
                fullpaths["sklearn"].add(path)
                fullpaths_all["sklearn"].append(path)
            elif 'torch' in path:
                packages["torch"].add(os.path.basename(path))
                fullpaths["torch"].add(path)
                fullpaths_all["torch"].append(path)
            elif 'cuda' in path:
                packages["cuda"].add(os.path.basename(path))
                fullpaths["cuda"].add(path)
                fullpaths_all["cuda"].append(path)
            elif 'h5py' in path:
                packages["h5py"].add(os.path.basename(path))
                fullpaths["h5py"].add(path)
                fullpaths_all["h5py"].append(path)
            elif 'locale' in path:
                packages["locale"].add(os.path.basename(path))
                fullpaths["locale"].add(path)
                fullpaths_all["locale"].append(path)
            elif 'lib' in path:
                packages["lib"].add(os.path.basename(path))
                fullpaths["lib"].add(path)
                fullpaths_all["lib"].append(path)
            else:
                #print(f"Unknown package: {path}")
                # Other files
                packages["other"].add(os.path.basename(path))
                fullpaths["other"].add(path)
                fullpaths_all["other"].append(path)
    print(f"Root count: {root_count}")
    #Sort fullpaths_all by number of duplicates
    for path, count in fullpaths_all.items():
        fullpaths_all[path] = sorted(count, key=lambda x: count.count(x), reverse=True)
    return packages, total_count, fullpaths, fullpaths_all

def analyze_packages(fullpaths, total_count):
    """Analyze package usage and create summary statistics."""
    package_stats = []
    
    for path, count in fullpaths.items():
        #print(f"Package: {package}")
        # Filter out empty subpackages
        #filtered_subpackages = [s for s in subpackages if s]
        
        # Count unique subpackages
            
        path_count = len(count)
        unique_count = len(np.unique(count))
        # if path == "root":
        #     #print(f"Root subpackages: {path}")
        #     #print(len(count))
        
        # Count total references (including duplicates)
        total_refs = path_count
        print(f'total_count: {total_count}, \ntotal_refs: {total_refs}')

        
        package_stats.append({
            'path': path,
            'path_count': path_count,
            'total_references': total_refs,
            'unique_count': unique_count,
            'percentage': (total_refs / total_count) * 100
        })
    
    # Sort by total references
    return sorted(package_stats, key=lambda x: x['total_references'], reverse=True)

def plot_package_stats(stats, output_file=None):
    """Create a visualization of package statistics."""
    # Get top packages by total references
    top_stats = stats[:10]  # Top 10 packages
    
    # Extract data for plotting
    packages = [s['path'] for s in top_stats]
    total_refs = [s['total_references'] for s in top_stats]
    unique_counts = [s['unique_count'] for s in top_stats]
    
    # Create figure with appropriate size
    plt.figure(figsize=(12, 8))
    
    # Set up bar positions
    x = np.arange(len(packages))
    width = 0.35
    
    # Create grouped bar chart
    plt.bar(x - width/2, total_refs, width, label='Total File Descriptors')
    plt.bar(x + width/2, unique_counts, width, label='Unique Components')
    
    # Add labels and title
    plt.xlabel('Package')
    plt.ylabel('Count')
    plt.title('File Descriptor Usage by Package')
    plt.xticks(x, packages, rotation=45, ha='right')
    plt.legend()
    
    # Add value labels on top of bars
    for i, v in enumerate(total_refs):
        plt.text(i - width/2, v + 5, str(v), ha='center')
    
    for i, v in enumerate(unique_counts):
        plt.text(i + width/2, v + 5, str(v), ha='center')
    
    plt.tight_layout()
    
    # Save or display
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

def main():
    parser = argparse.ArgumentParser(description='Analyze file descriptor usage by package')
    parser.add_argument('log_file', help='Path to the file descriptor log file')
    parser.add_argument('-o', '--output', help='Output file for the plot (optional)')
    parser.add_argument('--csv', help='Output CSV file for the statistics (optional)')
    args = parser.parse_args()
    
    packages, total_count, fullpaths, fullpaths_all = parse_fd_log(args.log_file)
    for path, count in fullpaths_all.items():
        print(f"{path}: {len(count)}")
    #print(f"Full paths: {fullpaths}")
    stats = analyze_packages(fullpaths_all, total_count)
    
    # Print summary
    print(f"Total file descriptors: {total_count}")
    print("\nTop packages by file descriptor count:")
    for i, pkg in enumerate(stats[:10], 1):
        print(f"{i}. {pkg['path']}: {pkg['total_references']} FDs ({pkg['percentage']:.1f}%), {pkg['path_count']} paths, {pkg['unique_count']} unique")
        #Print most duplicated path for each package
        print(f"Most duplicated path for {pkg['path']}: {fullpaths_all[pkg['path']][0]}")
    
    # Export to CSV if requested
    if args.csv:
        pd.DataFrame(stats).to_csv(args.csv, index=False)
        print(f"\nDetailed statistics saved to {args.csv}")
    
    # Create visualization
    plot_package_stats(stats, args.output)
    if args.output:
        print(f"Plot saved to {args.output}")

if __name__ == "__main__":
    main()