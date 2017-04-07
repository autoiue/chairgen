import peasy.*;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;

Voxel v;
Voxel next;
PeasyCam cam;
boolean flaggedRemoval = false;
int maxWidth, maxHeight, maxDepth = 0;
String rootPath = "/home/procsynth/LOCALDEV/";
String filepath = "";
int currentFile = 0;
ArrayList<String> files;

void setup(){
	size(1920, 1080, P3D);
	surface.setResizable(true);
	stroke(20);
	fill(150);
	strokeWeight(1);

	cam = new PeasyCam(this, 50, -100, 50, 300);

	cam.rotateY(radians(45));
	cam.rotateX(radians(25));

	cam.setSuppressRollRotationMode();
	cam.setResetOnDoubleClick(false);
	cam.setMinimumDistance(0);
	cam.setMaximumDistance(5000);

}

void draw(){

	background(200);

	stroke(200, 0, 0);
	line(0,0,0,100, 0, 0);
	stroke(0, 200, 0);
	line(0,0,0,0, -100, 0);
	stroke(0, 0, 200);
	line(0,0,0,0, 0, 100);
	stroke(20);
	if(flaggedRemoval)
		stroke(155,0,0);

	if(v != null){
		PVector p[] = v.points;
		for(int i = 0; i < p.length; i++){
			if(p[i] != null)
				point(p[i].x*1200,
				      -p[i].y*1200,
				      p[i].z*1200);
		} 
	}
}

public void keyReleased(){
	if(key == ESC || key == 's') {
	}else if (key == 'x') {
		flaggedRemoval = !flaggedRemoval;
	}else if (key == ' ' && files !=null) {
		if(flaggedRemoval){
			File bye = new File(files.get(currentFile));
			bye.delete();
			println("Removed "+files.get(currentFile));
		}
		flaggedRemoval = false;
		currentFile ++;
		if(currentFile >= files.size()){
			currentFile = 0;
		}
		v = next;
		try{
			next = new Voxel(files.get((currentFile+1)%files.size()));
		}catch(Exception e){
			e.printStackTrace();
		}
	}else if (key == 'r') {
		selectFolder("Select a folder to process:", "openFolder");
	}
}

public void openFolder(File folder){

	if(folder != null){

		File[] listOfFiles = folder.listFiles();

		files = new ArrayList<String>();

		for (int i = 0; i < listOfFiles.length; i++) {
			if (listOfFiles[i].isFile()) {
				if(listOfFiles[i].getName().endsWith(".xyz")){
					files.add(listOfFiles[i].getAbsolutePath());
				}
			}
		}

		println("Loaded "+ files.size() +" files.");

		currentFile = 0;

		if(files.size()>0)
			v = new Voxel(files.get(0));
		if(files.size()>1)	
			next = new Voxel(files.get(1));
	}

}
