Include "options01_data.geo";
Include "shape_functions.geo";
h=1/N;
PS_scat[] = {};
PSstore[] = {}; // array of Plane surface label
Centerstore[] = {};

BLx=-1;BLy=-1;TRx=1;TRy=1;PhysLab=10;isPhysical=0;
Call CreateRectangle;

cx=0;cy=0;r=0.2;PhysLab=20;isPhysical=1;CenterLab=-1;
Call CreateCircle;


For lab In {1:8}
  theta=lab*Pi/4;
  cx=0.5*Cos[theta];cy=0.5*Sin[theta];r=0.1;PhysLab=lab;CenterLab=-1;
  Call CreateCircle;// Plane surface label in PSstore[lab+1]
EndFor

Delete {
  Surface{PSstore[0]};
  Surface{PSstore[2]};
  Surface{PSstore[4]};
  Surface{PSstore[6]};
  Surface{PSstore[8]};
}

Plane Surface(PSstore[0]) = {1, 2, 3, 4, 5, 6, 7, 8, 10, 20};
Physical Surface(10) = {PSstore[0]};
