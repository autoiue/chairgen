import peasy.*;

Voxel v[];
int maxWidth, maxHeight, maxDepth = 0;
int blockX, blockY, blockZ, offset = 20;
PeasyCam cam;

void setup(){
	size(1920, 1080, P3D);
	surface.setResizable(true);
	println("Loading...");
	v = new Voxel[]{
		new Voxel("../../models/0001.json"),
		new Voxel("../../models/0002.json"),
		new Voxel("../../models/0003.json"),
		new Voxel("../../models/0004.json"),
		new Voxel("../../models/0005.json"),
		new Voxel("../../models/0006.json"),
		new Voxel("../../models/0007.json"),
		new Voxel("../../models/0008.json"),
		new Voxel("../../models/0009.json"),
		new Voxel("../../models/0010.json"),
		new Voxel("../../models/0011.json"),
		new Voxel("../../models/0013.json"),
		new Voxel("../../models/0015.json"),
		new Voxel("../../models/0016.json"),
		new Voxel("../../models/0018.json"),
		new Voxel("../../models/0019.json")
	};

	for (int i = 0; i < v.length; i++) {
		maxWidth = Math.max(maxWidth, v[i].getWidth());
		maxHeight = Math.max(maxHeight, v[i].getHeight());
		maxDepth = Math.max(maxDepth, v[i].getDepth());
	}


	blockX = (int) random(10, 20);
	blockY = (int) random(10, 30);
	blockZ = (int) random(10, 30);
	offset = (int) random(v.length);

	stroke(20);
	fill(150);
	strokeWeight(0.5);

	cam = new PeasyCam(this, 0, 200, 0, 1000);

	cam.rotateX(radians(25));

	cam.setSuppressRollRotationMode();
	cam.setResetOnDoubleClick(false);
	cam.setMinimumDistance(0);
	cam.setMaximumDistance(5000);

}

void draw(){
	if(keyPressed && key == ' '){
		blockX = (int) random(10, 20);
		blockY = (int) random(10, 40);
		blockZ = (int) random(8, 30);
		offset = (int) random(v.length);
	}

	background(200);
	for(int x = -maxWidth/2; x < maxWidth/2; x++){
		for(int y = -maxHeight/2; y < maxHeight/2; y++){
			for(int z = -maxDepth/2; z < maxDepth/2; z++){
				int pick = (int) (maxDepth+maxHeight+maxWidth+((x/blockX)+(y/blockY)+(z/blockZ))+offset) % v.length;
				if(v[pick].get(x, y, z)){
					pushMatrix();
					translate(x*10, -y*10, z*10);
					box(10);
					popMatrix();
				}
			}
		}
	}
	
}