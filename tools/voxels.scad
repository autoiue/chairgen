echo(version=version());


module voxel(x, y, z){
	translate([x*10, y*10, z*10]) cube(12, center = true);
}