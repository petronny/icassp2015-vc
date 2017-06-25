straight_path='STRAIGHT_PATH'
wavfile='WAVFILE'

addpath(straight_path);
opts.F0defaultWindowLength  = 25;
opts.F0frameUpdateInterval  = 5;
opts.F0searchLowerBound     = 50;
opts.F0searchUpperBound     = 600;
opts.defaultFrameLength     = 25;
opts.spectralUpdateInterval = 5;
[x,fs] = audioread(wavfile);
[f0,ap]=exstraightsource(x,fs,opts);
sp=exstraightspec(x,f0,fs,opts);
lf0=log(f0);
ap=ap';
sp=sp'*32768.0;
save([wavfile(1:length(wavfile)-3) 'lf0.csv'], 'lf0', '-ascii');
save([wavfile(1:length(wavfile)-3) 'ap.csv'], 'ap', '-ascii');
save([wavfile(1:length(wavfile)-3) 'sp.csv'], 'sp', '-ascii');
exit
