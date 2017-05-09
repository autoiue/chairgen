echo(version=version());
seed = 42;

module primitive(u){
	rotate([0,60,-25]){	
		union() {
			sphere(r = u);
			translate([0, 0, u * sin(30)])
			cylinder(h = 1.5*u, r1 = u * cos(30), r2 = 0);
		}
	}
}

module atom(x, y, z){
	if(rands(0,1,1,seed)[0]>0.9){
		translate([x*40, y*40, z*40]){
			primitive(4);
		}
	}
}
