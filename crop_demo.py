from ObjectDetectionDataset import *

def main():
 # Define the path to images and annotations
 images_path = os.path.join(os.getcwd(), "tests", "cars_dataset", "images")
 annotations_path = os.path.join(os.getcwd(), "tests", "cars_dataset", "annotations", "xmls")
 # Define the name of the dataset
 dbName = "CarsDataset"
 # Create an object of ObjectDetectionDataset
 imda = ObjectDetectionDataset(imagesDirectory = images_path, annotationsDirectory = annotations_path, databaseName = dbName)
 # Reduce the dataset to smaller Rois of smaller ROIs of shape 1032x1032.
 images_output_path = os.path.join(os.getcwd(), "tests", "cars_dataset", "images_reduced")
 annotations_output_path = os.path.join(os.getcwd(), "tests", "cars_dataset", "annotations_reduced", "xmls")
 imda.reduceDatasetByRois(offset = [1032, 1032], outputImageDirectory = images_output_path, outputAnnotationDirectory = annotations_output_path)

if __name__ == "__main__":
 main()
