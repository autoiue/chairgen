import processing.core.*;

public class Voxel{

	public PVector points[];
	
	public Voxel(String file){

		String lines[] = loadStrings(file);

		points = new PVector[lines.length];
		println("Loading "+file+" with "+lines.length+" points ...");
		
		for(int i = 0; i < lines.length ; i++){
			String pos[] = lines[i].split(" ");
			if(pos.length >= 3){
				points[i] = new PVector(Float.parseFloat(pos[0]),Float.parseFloat(pos[1]), Float.parseFloat(pos[2]));
			}
		}


		println("Loaded "+points.length+" points ...");

	}


}