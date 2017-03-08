import processing.core.*;

public class Voxel{

private boolean voxel[][][];
private int width, height, depth;
	
	public Voxel(String file){
		JSONObject json = loadJSONObject(file);
		JSONObject dim = json.getJSONArray("dimension").getJSONObject(0);
		JSONArray vxs = json.getJSONArray("voxels");

		width = dim.getInt("width")+1;
		height = dim.getInt("height")+1;
		depth = dim.getInt("depth")+1;

		voxel = new boolean[width][height][depth];

		for(int i = 0; i < vxs.size() ; i++){
			voxel
			[vxs.getJSONObject(i).getInt("x")]
			[vxs.getJSONObject(i).getInt("y")]
			[vxs.getJSONObject(i).getInt("z")]
			 = true;
		}
	}

	public int getWidth(){return width;}
	public int getHeight(){return height;}
	public int getDepth(){return depth;}

	public boolean get(int x, int y, int z){
		x += width/2;
		y += height/2;
		z += depth/2;

		if(0 < x && x < width &&
		   0 < y && y < height &&
		   0 < z && z < depth){
		   	return voxel[x][y][z];
		}else{
			return false;
		}
	}
}