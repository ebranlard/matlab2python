%% Initialization
clear all; close all; clc; % addpath()

%% Spectrum

dt=0.1
t=0:dt:1;
y=sin(t)
[S,f]=fSpectrum(y,length(y),1/dt);

S_ref=[0.2285364   0.0258482   0.0066528   0.0033719   0.0023203   0.0019575]
f_ref=[0.00000   0.90909   1.81818   2.72727   3.63636   4.54545]
