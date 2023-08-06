# Based on http://www.fon.hum.uva.nl/praat/manual/Script_for_listing_time_--F0_--intensity.html
#

form Soundfile to pitch and intensity
    sentence Input_audio_file_name C:\Users\Tim\Dropbox\workspace\praatIO\examples\files\bobby.wav
    sentence Output_data_file_name C:\Users\Tim\Dropbox\workspace\praatIO\examples\files\pitch_extraction\pitch\bobby.txt
    real Sample_step 0.01
    real Min_pitch 75
    real Max_pitch 450
    real Silence_threshold 0.03
    real Start_time -1 (= start of the file)
    real End_time -1 (= end of the file)
    boolean Do_pitch_quadratic_interpolation 0
endform

# Pitch and intensity parameters
# male: 50, 350
# female: 75, 450

# Load audio file
sound = Read from file: input_audio_file_name$
selectObject: sound


# Set the start and end times
if start_time < 0
	tmin = Get start time
else
	tmin = start_time
endif

if end_time <= 0
	tmax = Get end time
else
	tmax = end_time
endif


# Get pitch track
pitch = To Pitch (ac): sample_step, min_pitch, 15, "no", silence_threshold, 0.45, 0.01, 0.35, 0.14, max_pitch

# Do quadratic interpolation if requested
if do_pitch_quadratic_interpolation == 1
    old_pitch = pitch
    selectObject: pitch
    pitchTier = Down to PitchTier
    
    selectObject: pitchTier
    Interpolate quadratically: 4, "Hz"
    pitch = To Pitch: sample_step, min_pitch, max_pitch
    
    selectObject: pitchTier
    Remove
    selectObject: old_pitch
    Remove
endif

# Get intensity track
selectObject: sound
intensity = To Intensity: min_pitch, sample_step, 1

table = Create Table with column names: "table", 0, "time pitch intensity"

# Iterate over the pitch and intensity tracks, one sample at a time
for i to (tmax - tmin) / sample_step
	time = tmin + i * sample_step
	selectObject: pitch
	pitchVal = Get value at time: time, "Hertz", "Linear"
	selectObject: intensity
	intensityVal = Get value at time: time, "Cubic"
	
	selectObject: table
	Append row
	current_row = Get number of rows
  	Set numeric value: current_row, "time", time
  	Set numeric value: current_row, "pitch", pitchVal
  	Set numeric value: current_row, "intensity", intensityVal
endfor

Save as comma-separated file: output_data_file_name$

# Cleanup
selectObject: pitch
Remove

selectObject: intensity
Remove

selectObject: sound
Remove

selectObject: table
Remove
