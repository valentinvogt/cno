#!/usr/bin/env python3
"""
CNO Model Evaluation Results Parser and Plotter

This script parses CNO model evaluation output files and creates plots
showing relative and L1 absolute errors for different testing patterns.

Usage:
    python cno_eval_plotter.py <path_to_out_file>
"""

import re
import sys
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import argparse

def parse_cno_output(file_path):
    """
    Parse the CNO evaluation output file and extract error data.
    
    Args:
        file_path (str): Path to the .out file
        
    Returns:
        dict: Dictionary with pattern names as keys and error data as values
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Dictionary to store results for each pattern
    patterns_data = {}
    
    # Split content by testing patterns
    pattern_sections = re.split(r'Testing pattern (\[.*?\])', content)
    
    # Process each pattern section
    for i in range(1, len(pattern_sections), 2):
        pattern_str = pattern_sections[i]
        pattern_data = pattern_sections[i + 1]
        
        # Parse pattern string to get the actual pattern
        pattern = eval(pattern_str)  # Convert string representation to list
        pattern_name = str(pattern)
        
        # Initialize data structure for this pattern
        patterns_data[pattern_name] = {
            'steps': [],
            'relative_errors': [],
            'l1_errors': []
        }
        
        # Find all error entries in this pattern section
        # Look for lines with format: "number number error_value L1 error"
        # Only consider component 0 (first component)
        error_lines = re.findall(r'(\d+)\s+0\s+([\d.]+)\s+L1 error', pattern_data)
        
        for step, l1_error in error_lines:
            step_num = int(step)
            # Fix indexing: if step is 6, it should be 7 (final step)
            if step_num == 6:
                step_num = 7
            l1_val = float(l1_error)
            
            # Store step and L1 error
            patterns_data[pattern_name]['steps'].append(step_num)
            patterns_data[pattern_name]['l1_errors'].append(l1_val)
        
        # Find relative errors (lines ending with just a number, not "L1 error")
        # Only consider component 0 (first component)
        relative_error_lines = re.findall(r'(\d+)\s+0\s+([\d.]+)(?!\s+L1 error)', pattern_data)
        
        for step, rel_error in relative_error_lines:
            step_num = int(step)
            # Fix indexing: if step is 6, it should be 7 (final step)
            if step_num == 6:
                step_num = 7
            rel_val = float(rel_error)
            
            patterns_data[pattern_name]['relative_errors'].append(rel_val)
    
    # Clean up and organize data
    for pattern_name in patterns_data:
        data = patterns_data[pattern_name]
        if data['steps'] and data['relative_errors'] and data['l1_errors']:
            # Create matched pairs of steps with their corresponding errors
            step_rel_pairs = list(zip(data['steps'][:len(data['relative_errors'])], data['relative_errors']))
            step_l1_pairs = list(zip(data['steps'][:len(data['l1_errors'])], data['l1_errors']))
            
            # Sort by step number
            step_rel_pairs.sort(key=lambda x: x[0])
            step_l1_pairs.sort(key=lambda x: x[0])
            
            # Update the data structure
            data['steps'] = [pair[0] for pair in step_rel_pairs]
            data['relative_errors'] = [pair[1] for pair in step_rel_pairs]
            data['l1_errors'] = [pair[1] for pair in step_l1_pairs]
    
    return patterns_data

def plot_errors(patterns_data, output_prefix='cno_eval'):
    """
    Create plots for relative and L1 absolute errors.
    
    Args:
        patterns_data (dict): Parsed error data
        output_prefix (str): Prefix for output files
    """
    # Set up the plotting style
    plt.style.use('default')
    fig_size = (12, 5)
    
    # Create relative error plot
    plt.figure(figsize=fig_size)
    for pattern_name, data in patterns_data.items():
        if data['relative_errors'] and not all(np.isnan(data['relative_errors'])):
            plt.plot(data['steps'], data['relative_errors'], 'o-', label=f'Pattern {pattern_name}', linewidth=2, markersize=6)
    
    plt.xlabel('Time Step', fontsize=12)
    plt.ylabel('Relative Error (%)', fontsize=12)
    plt.title('CNO Model: Relative Error by Pattern', fontsize=14, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_relative_errors.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    # Create L1 absolute error plot
    plt.figure(figsize=fig_size)
    for pattern_name, data in patterns_data.items():
        if data['l1_errors'] and not all(np.isnan(data['l1_errors'])):
            plt.plot(data['steps'], data['l1_errors'], 'o-', label=f'Pattern {pattern_name}', linewidth=2, markersize=6)
    
    plt.xlabel('Time Step', fontsize=12)
    plt.ylabel('L1 Absolute Error', fontsize=12)
    plt.title('CNO Model: L1 Absolute Error by Pattern', fontsize=14, fontweight='bold')
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f'{output_prefix}_l1_errors.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    parser = argparse.ArgumentParser(description='Parse and plot CNO model evaluation results')
    parser.add_argument('input_file', help='Path to the .out file containing evaluation results')
    parser.add_argument('--output-prefix', default='cno_eval', help='Prefix for output plot files')
    
    args = parser.parse_args()
    
    try:
        # Parse the output file
        print(f"Parsing CNO evaluation results from: {args.input_file}")
        patterns_data = parse_cno_output(args.input_file)
        
        if not patterns_data:
            print("No pattern data found in the file. Please check the file format.")
            return
        
        # Print summary
        print(f"\nFound {len(patterns_data)} testing patterns:")
        for pattern_name, data in patterns_data.items():
            n_steps = len([x for x in data['steps'] if not np.isnan(x)])
            n_rel_errors = len([x for x in data['relative_errors'] if not np.isnan(x)])
            n_l1_errors = len([x for x in data['l1_errors'] if not np.isnan(x)])
            print(f"  {pattern_name}: {n_steps} steps, {n_rel_errors} relative errors, {n_l1_errors} L1 errors")
        
        # Create plots
        print("\nGenerating plots...")
        plot_errors(patterns_data, args.output_prefix)
        print(f"Plots saved as {args.output_prefix}_relative_errors.png and {args.output_prefix}_l1_errors.png")
        
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    main()