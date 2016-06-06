L = 24;
A = zeros(L,L,3);

for i = 1:L
    for j = 1:L
        A(i,j,1) = i*8 + j;
        A(i,j,2) = i + j*2;
        A(i,j,3) = i + j*3;
    end
end


A = uint8(A);
imwrite(A,'24x24.ppm');
imwrite(A,'24x24.bmp');
imwrite(A,'24x24.jpg');

R = A(:,:,1);
G = A(:,:,2);
B = A(:,:,3);

n2_blue_block = A(1:8,9:16,3);
csvwrite('n2_blue_block.csv', n2_blue_block);

n1_red_block = A(1:8, 1:8, 1);
csvwrite('n1_red_block.csv',n1_red_block);

n9_green_block = A(17:24, 17:24, 2);
csvwrite('n9_green_block.csv', n9_green_block);
