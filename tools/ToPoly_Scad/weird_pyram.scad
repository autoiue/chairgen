echo(version=version());


module atom(x, y, z){
	s=3;
	translate([x*100, y*100, z*100]){
		polyhedron(
				   points=[
				   [s,s,0],
				   [s,-s,0],
				   [0,-s,0.5*s],
				   [-s,0.2*s,0.3*s],
				   [0,0,s]
				   ],
				   faces=[
				   [0,1,4],
				   [1,2,4],
				   [2,3,4],
				   [3,0,4],
				   [1,0,3],
				   [2,1,3]
				   ]
				   );
	}
}