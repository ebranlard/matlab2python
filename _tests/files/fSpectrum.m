function [Sp,vf]=fSpectrum(y,N,fs)
y  = y(:)';
vf = (0:N/2)*fs/N    ;
vf = (0:floor(N/2))*fs/N    ;
Sp = abs(fft(y)).^2 / (N*fs);
Sp = Sp(1:floor(N/2)+1)     ;

