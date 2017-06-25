straight_path='STRAIGHT_PATH'
wavfile='WAVFILE'
model='MODEL'

addpath(straight_path);
opts.F0defaultWindowLength  = 25;
opts.F0frameUpdateInterval  = 5;
opts.F0searchLowerBound     = 50;
opts.F0searchUpperBound     = 600;
opts.defaultFrameLength     = 25;
opts.spectralUpdateInterval = 5;
ap=load([wavfile(1:length(wavfile)-3) 'ap.csv'], '-ascii');
sp=load([wavfile(1:length(wavfile)-3) 'sp.csv'], '-ascii');
lf0=exp(f0);
ap=ap';
sp=sp'/32768.0;
source_lf0=load([wavfile(1:length(wavfile)-3) 'lf0.csv'], '-ascii');
target_lf0=load(strrep([wavfile(1:length(wavfile)-3) 'lf0.csv'],'awb','slt'), '-ascii');
source_lf0=source_lf0-mean(source_lf0)
source_lf0=source_lf0/var(source_lf0)
source_lf0=source_lf0*var(target_lf0)
source_lf0=source_lf0+mean(target_lf0)
[f0,ap]=exstraightsource(x,fs,opts);
[x,fs] = audioread(wavfile);
sp=exstraightspec(x,f0,fs,opts);
exit
