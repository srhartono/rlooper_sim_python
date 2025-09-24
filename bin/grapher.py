import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse as args

def parse_arg():
	myargs = args.ArgumentParser(description='R-loop Peak Simulator')
	myargs.add_argument('-i','--input', type=str, help='Input peak file (CSV)')
	myargs.add_argument('-o','--output', type=str, help='Output graph file (PNG)')
	return myargs.parse_args()

def main():
    myargs = parse_arg()
    if myargs.input:
        try:
            print(f"Reading peaks from: {myargs.input}")
            peaks = pd.read_csv(myargs.input, sep='\t')  # Use tab separator for CSV files from rlooper
            print(f"Loaded {len(peaks)} peaks")
            print(f"Columns: {list(peaks.columns)}")
        except Exception as e:
            print(f"Error reading input file: {e}")
            return
    else:
        print("\nUsage: grapher.py -i <input_peak_file> -o <output_graph_file>")
        return
    
    if myargs.output:
        output_file = myargs.output
    else:
        output_file = 'rloop_peaks.png'
    
    print(f"Creating graph: {output_file}")
    try:
        graph_compressed_pileup(peaks, output_file)
    except Exception as e:
        print(f"Error creating graph: {e}")
        import traceback
        traceback.print_exc()

def find_pileup_level(start, end, occupied_levels):
	"""Find the lowest available level for a peak, allowing proper pileup"""
	# Try to place in existing levels first
	for level in range(len(occupied_levels)):
		# Check if this peak can fit in this level (no overlap with existing peaks)
		can_fit = True
		for occupied_start, occupied_end in occupied_levels[level]:
			# Check for overlap: peaks overlap if they don't end before the other starts
			if not (end <= occupied_start or start >= occupied_end):
				can_fit = False
				break
		
		if can_fit:
			occupied_levels[level].append((start, end))
			return level
	
	# If no existing level works, create a new level
	occupied_levels.append([(start, end)])
	return len(occupied_levels) - 1

def graph_compressed_pileup(peaks, output_file='rloop_peaks.png'):
	plt.figure(figsize=(16, 8))
	
	# Sort peaks by start position, then by end position
	peaks_sorted = peaks.sort_values(['start', 'end']).reset_index(drop=True)
	
	# Create proper pileup: overlapping peaks get stacked
	levels = []  # Each element is list of (start, end, prob, original_index)
	
	# Create pileup array covering the genomic range
	min_pos = 0 #peaks_sorted['start'].min()
	max_pos = peaks_sorted['end'].max()*2
	pileup_size = max_pos - min_pos + 1
	pileup = [0] * pileup_size  # Initialize with zeros
	
	for idx, row in peaks_sorted.iterrows():
		start = row['start']
		end = row['end'] 
		prob = row['probability']
		# Count coverage for each position in the peak
		for i in range(start, end + 1):
			pileup[i - min_pos] += 1  # Adjust for array indexing

		# # Find the first level where this peak can fit (no overlap)
		# placed = False
		# for level_idx, level_intervals in enumerate(levels):
		# 	# Check if peak overlaps with any interval in this level
		# 	overlaps = False
		# 	for interval_start, interval_end, _, _ in level_intervals:
		# 		if not (end <= interval_start or start >= interval_end):  # They overlap
		# 			overlaps = True
		# 			break
			
		# 	if not overlaps:  # Can place in this level
		# 		levels[level_idx].append((start, end, prob, idx))
		# 		placed = True
		# 		break
		
		# if not placed:  # Need new level
		# 	levels.append([(start, end, prob, idx)])
		# 	if len(levels) <= 5:  # Debug first few levels
		# 		print(f"Created level {len(levels)-1} for peak {idx}: {start}-{end}")
	
	# Draw the pileup
	# for level_idx, level_intervals in enumerate(levels):
	# 	for start, end, prob, orig_idx in level_intervals:
	# 		# Use probability for color intensity  
	# 		color_intensity = prob / peaks['probability'].max()  # Normalize to 0-1
	# 		height = 0.8
			
	# 		# Draw horizontal block
	# 		plt.barh(level_idx, end - start, left=start, height=height, 
	# 				color=plt.cm.viridis(color_intensity), 
	# 				alpha=0.85, edgecolor='navy', linewidth=0.3)
			
	# 		# Add probability label
	# 		mid_pos = (start + end) / 2
	# 		plt.text(mid_pos, level_idx, f'{prob:.3f}', 
	# 				ha='center', va='center', fontsize=7, 
	# 				color='white' if color_intensity > 0.5 else 'black',
	# 				weight='bold')
	# Create x-axis positions (genomic coordinates)
	x_positions = range(min_pos, max_pos + 1)
	
	# Create line plot for pileup coverage
	plt.plot(x_positions, pileup, 'b-', linewidth=2, alpha=0.8, label='Coverage')
	
	# Optional: Add filled area under the curve
	plt.fill_between(x_positions, pileup, alpha=0.3, color='lightblue')
	
	# Optional: Add scatter points for peaks
	plt.scatter(x_positions, pileup, s=10, alpha=0.6, color='darkblue')
	
	plt.xlabel('Genomic Position (bp)')
	plt.ylabel('Peak Coverage Depth')
	plt.title(f'PEAK: {len(peaks_sorted)} peaks')
	plt.grid(True, alpha=0.3)
	plt.legend()
	
	plt.tight_layout()
	plt.savefig(output_file, dpi=300, bbox_inches='tight')
	plt.close()
	# Set y-axis to show all levels with some padding
	# plt.ylim(-0.5, len(levels) - 0.5)
	
	# # Add colorbar
	# sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=plt.Normalize(vmin=0, vmax=peaks['probability'].max()))
	# sm.set_array([])
	# cbar = plt.colorbar(sm, ax=plt.gca())
	# cbar.set_label('R-loop Formation Probability', rotation=270, labelpad=20)
	
	# # Calculate pileup stats
	# peaks_per_level = [len(level) for level in levels]
	# max_pileup = max(peaks_per_level)
	# avg_pileup = sum(peaks_per_level) / len(peaks_per_level)
	
	# plt.tight_layout()
	# plt.savefig(output_file, dpi=300, bbox_inches='tight')
	# plt.close()
	
	# print(f"✅ Graph saved to {output_file}")
	# print(f"📊 Pileup complete: {len(peaks_sorted)} peaks → {len(levels)} levels")
	# print(f"�️  Max pileup depth: {max_pileup} peaks/level")
	# print(f"📈 Average: {avg_pileup:.1f} peaks/level") 
	return

if __name__ == "__main__":
	main()
