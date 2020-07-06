%
%  Discrete Fourier Transform
%
function Xk = dft(x)
[N,M] = size(x);
if M ~=1,   % makes sure that x is a column vector
  x = x';
  N = M;
end
Xk=zeros(N,1);
n = 0:N-1;
for k=0:N-1
  Xk(k+1) = exp(-j*2*pi*k*n/N)*x;
end