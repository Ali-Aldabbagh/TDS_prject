  #include <ros/ros.h>
  // PCL specific includes
  #include <sensor_msgs/PointCloud2.h>
  #include <pcl_conversions/pcl_conversions.h>
  #include <pcl/point_cloud.h>
  #include <pcl/point_types.h>

  #include <pcl/filters/voxel_grid.h>


  // STL
#include <iostream>
#include <limits>

// PCL
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/filters/filter.h>
#include <pcl/filters/extract_indices.h>

#include <pcl/common/transforms.h>


#include <iostream>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/filters/statistical_outlier_removal.h>
  ros::Publisher pub;

   
   void cloud_cb(const boost::shared_ptr<const sensor_msgs::PointCloud2>& input){
    
    pcl::PCLPointCloud2* cloud = new pcl::PCLPointCloud2;
     pcl::PCLPointCloud2ConstPtr cloudPtr(cloud);
    // Container for original & filtered data
      pcl::PCLPointCloud2 pcl_pc2;

     pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud_filtered(new pcl::PointCloud<pcl::PointXYZRGB>);
     pcl::PointCloud<pcl::PointXYZRGB>::Ptr outputCloud(new pcl::PointCloud<pcl::PointXYZRGB>);
     pcl_conversions::toPCL(*input,pcl_pc2);

     
     

    pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud(new pcl::PointCloud<pcl::PointXYZRGB>);
    pcl::fromPCLPointCloud2(pcl_pc2,*temp_cloud);

    // Perform the actual filtering
     pcl::VoxelGrid<pcl::PointXYZRGB> sor;
     sor.setInputCloud (temp_cloud);
     sor.setLeafSize (0.04f, 0.04f, 0.04f); //(0.04) defult
     sor.filter (*cloud_filtered); 
     //cloud_filtered=temp_cloud;

     //==================================================================================
      std::cout << "sizein: \n " << temp_cloud->points.size () << std::endl; 
  //    pcl::StatisticalOutlierRemoval<pcl::PointXYZRGB> soro;   //Create filter object
	//    soro.setInputCloud(cloud_filtered);                           //Set point cloud to be filtered
  //    soro.setMeanK(50);                               //Set the number of query point proximity points to be considered in Statistics
  //    soro.setStddevMulThresh(0.1); // set the threshold to determine whether it is an outlier
  //  //soro.setStddevMulThresh(0.00034);                      //Set threshold to judge whether it is outlier 0.0000000001
  // 	 soro.filter(*cloud_filtered);                    //storage
     
     //=====================================================================

     //pcl::PointCloud<pcl::PointXYZ>::Ptr p_obstacles(new pcl::PointCloud<pcl::PointXYZ>);
     pcl::PointIndices::Ptr inliers(new pcl::PointIndices());
     pcl::ExtractIndices<pcl::PointXYZRGB> extract;
      


     float x,y,z,i;
      
      
     for (size_t i = 0; i < cloud_filtered->points.size (); ++i)  {   
     x=cloud_filtered->points[i].x;
     
     //cloud_filtered->points[i].g=0;
     //cloud_filtered->points[i].b=0;
     if( x>=-0.6 && x<=0.6) { //x>=-0.6 &&x<=0.6
                             // if(z<=1.5 && ((x>=-0.05 && x<=0.05)|| (x>=0.2 && x<=0.3)||(x>=-0.3 && x<=-0.2))) /=> three strips
       

        }else{
        inliers->indices.push_back(i);
         //   std::cout << " x= " << x << std::endl;  

         //cloud_filtered->points[i].x=NAN;
        // cloud_filtered->points[i].y=NAN;
        // cloud_filtered->points[i].z=NAN;
          
    }
     }
     
   
     
     
     
    
    
   extract.setInputCloud(cloud_filtered);
   extract.setIndices(inliers);
   extract.setNegative(true);
   extract.filter(*cloud_filtered);

    std::cout << "sizeout: \n " << cloud_filtered->points.size () << std::endl;
    
  
    //std::vector<int> indices;
    //pcl::removeNaNFromPointCloud(*cloud_filtered, *outputCloud, indices);
     





 //+=========================JUST FOR THE NEW BOT===========================================
     // Eigen::Matrix4f transform_1 = Eigen::Matrix4f::Identity();
  //> float theta2 =-M_PI/6; // M_PI/2 The angle of rotation in radians
  //> float theta3 =-0.58; // M_PI/2 The angle of rotation in radians
  // transform_1 (0,0) = std::cos (theta);
   //transform_1 (0,1) = -sin(theta);
   //transform_1 (1,0) = sin (theta);
  // transform_1 (1,1) = std::cos (theta);


  //>Eigen::Affine3f transform_2 = Eigen::Affine3f::Identity();
  //>Eigen::Affine3f transform_3 = Eigen::Affine3f::Identity();
  // Define a translation of 2.5 meters on the x axis.
  //transform_2.translation() << 2.5, 0.0, 0.0;

  // The same rotation matrix as before; theta radians around Z axis
  //>transform_2.rotate (Eigen::AngleAxisf (theta2, Eigen::Vector3f::UnitX()));
  //>transform_3.rotate (Eigen::AngleAxisf (theta3, Eigen::Vector3f::UnitY()));
   
   // Executing the transformation
   //>  pcl::PointCloud<pcl::PointXYZRGB>::Ptr transformed_cloud (new pcl::PointCloud<pcl::PointXYZRGB> ());
   // You can either apply transform_1 or transform_2; they are the same
   //> pcl::transformPointCloud (*cloud_filtered, *transformed_cloud, transform_2);
   //> cloud_filtered=transformed_cloud;
   //> pcl::transformPointCloud (*cloud_filtered, *transformed_cloud, transform_3);
   //> cloud_filtered=transformed_cloud; 
 //==============================================================================
     
     
      //publishing the data
     pcl::PCLPointCloud2 cloudB;
     pcl::toPCLPointCloud2(*cloud_filtered,cloudB);//cloud_filtered

     // Convert to ROS data type

     //cloud_normals->points.size ()

     sensor_msgs::PointCloud2 output;

     pcl_conversions::moveFromPCL(cloudB, output);
     // Publish the data.

     //usleep(100000); 
     pub.publish (output);



     

    //-------------------

   
   }

   int
   main (int argc, char** argv)
   {
     // Initialize ROS
     ros::init (argc, argv, "cdsacnode");
     ros::NodeHandle nh;

     // Create a ROS subscriber for the input point cloud
     ros::Subscriber sub = nh.subscribe ("/camera/depth/color/points", 1, cloud_cb);///camera1/depth/points

     // Create a ROS publisher for the output point cloud
     pub = nh.advertise<sensor_msgs::PointCloud2> ("cdsac", 1);

     // Spin
     ros::spin ();
   }
