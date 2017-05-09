echo(version=version());


module atom(x, y, z){
	translate([x*40, y*40, z*40]){
		if(rands(0,1,1)[0]>0.9){
			rotate([0,60,-25])cylinder(h = 6, r1 = 4, r2 = 0);
		}
	}
}
