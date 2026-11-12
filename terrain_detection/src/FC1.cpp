
#include <ros/ros.h>
// PCL specific includes
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>

#include <pcl/io/pcd_io.h>

#include <pcl/impl/point_types.hpp>

#include <pcl/features/normal_3d.h>

#include <pcl/visualization/cloud_viewer.h>

#include <pcl/point_types.h>
#include <pcl/features/normal_3d.h>
#include <pcl/io/pcd_io.h>

#include <pcl/visualization/cloud_viewer.h>

#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_types.h>
#include <pcl/PCLPointCloud2.h>
#include <pcl/conversions.h>
#include <pcl_ros/transforms.h>

#include <pcl_ros/point_cloud.h>
#include <math.h>
#include <stdio.h>

#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/filters/filter.h>
#include <pcl/filters/extract_indices.h>

#include <pcl/sample_consensus/ransac.h>
#include <pcl/sample_consensus/sac_model_plane.h>
#include <pcl/sample_consensus/sac_model_sphere.h>

#include <iostream>
#include <vector>

#include <pcl/search/search.h>
#include <pcl/search/kdtree.h>
#include <pcl/features/normal_3d.h>
#include <pcl/visualization/cloud_viewer.h>
#include <pcl/filters/passthrough.h>
#include <pcl/segmentation/region_growing.h>

#include <pcl/sample_consensus/model_types.h>
#include <pcl/segmentation/sac_segmentation.h>

#include <pcl/io/openni_grabber.h>
#include <pcl/visualization/cloud_viewer.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/segmentation/extract_clusters.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/kdtree/kdtree.h>
#include <pcl/common/common.h>
#include <pcl/common/transforms.h>
#include <pcl/segmentation/region_3d.h>

#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include "terrain_detection/cent.h"

#include <pcl/common/common_headers.h>
#include <pcl/range_image/range_image.h>
#include <pcl/io/pcd_io.h>
#include <pcl/visualization/range_image_visualizer.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <pcl/console/parse.h>

#include <pcl/range_image/range_image.h>

#include <message_filters/subscriber.h>
#include <message_filters/synchronizer.h>
#include <message_filters/sync_policies/approximate_time.h>
#include <sensor_msgs/Image.h>
#include "sensor_msgs/Imu.h"

#include <unistd.h>

#include "terrain_detection/Classifier.h"
//#include "pythonode/AddTwoInts.h"

using namespace sensor_msgs;
using namespace message_filters;

//float avaimu=0;
//int es=0;

ros::Publisher pub;
ros::Publisher pubm;

void cloud_cb(const boost::shared_ptr<const sensor_msgs::PointCloud2> &input, const sensor_msgs::Imu::ConstPtr &imu)
{

  ros::WallTime start_, end_;

  start_ = ros::WallTime::now();

  // **** do something here... ****

  //ROS_INFO("Imu Orientation x: [%f], y: [%f], z: [%f], w: [%f]", imu->orientation.x,imu->orientation.y,imu->orientation.z,imu->orientation.w);
  double r, p, y;
  float roll = 0, angch = 0;
  tf::Quaternion quat;
  tf::quaternionMsgToTF(imu->orientation, quat);
  tf::Matrix3x3(quat).getRPY(r, p, y);
  roll = r;
  p = p * 180 / 3.14;

  angch = (roll * 180 / 3.14) + 180;
  //std::cerr << "angch= " << angch << std::endl;
  // if(es<10){
  //  avaimu=roll+avaimu;
  //   es=es+1;
  //  }else{
  //  roll=avaimu/10;

  //  }

  pcl::PCLPointCloud2 pcl_pc2;
  pcl_conversions::toPCL(*input, pcl_pc2);

  pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud(new pcl::PointCloud<pcl::PointXYZRGB>);
  //pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloudx(new pcl::PointCloud<pcl::PointXYZRGB>);
  // pcl::PointCloud<pcl::PointXYZ>::Ptr final(new pcl::PointCloud<pcl::PointXYZ>);
  pcl::fromPCLPointCloud2(pcl_pc2, *temp_cloud);
  //temp_cloudx=temp_cloud;

  if (angch <= 180 && angch >= 0)
  {
    angch = (angch - 90) * -1;
    //es=0;
    angch = angch ;
    //===========Test downsampling=========================================

    //pcl::PointCloud<pcl::PointXYZRGB>::Ptr ds_cloud(new pcl::PointCloud<pcl::PointXYZRGB>);
    // Perform the actual filtering
    //pcl::VoxelGrid<pcl::PointXYZRGB> sor;
    //sor.setInputCloud (temp_cloud);
    //sor.setLeafSize (0.03f, 0.03f, 0.03f);
    //sor.filter (*ds_cloud);
    //temp_cloud=ds_cloud;
    //===============================================

    //do stuff with temp_cloud here
    pcl::NormalEstimation<pcl::PointXYZRGB, pcl::Normal> ne;
    ne.setInputCloud(temp_cloud);

    // Create an empty kdtree representation, and pass it to the normal estimation object.
    // Its content will be filled inside the object, based on the given input dataset (as no other search surface is given).
    pcl::search::KdTree<pcl::PointXYZRGB>::Ptr tree(new pcl::search::KdTree<pcl::PointXYZRGB>());
    ne.setSearchMethod(tree);

    // Output datasets
    pcl::PointCloud<pcl::Normal>::Ptr cloud_normals(new pcl::PointCloud<pcl::Normal>);

    // Use all neighbors in a sphere of radius 3cm
    ne.setKSearch(10); //=====>>>>>>>>>>>>>>>>>>>REDUIS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>10

    // Compute the features
    ne.compute(*cloud_normals);

    pcl::RegionGrowing<pcl::PointXYZRGB, pcl::Normal> reg;
    reg.setMinClusterSize(50);
    reg.setMaxClusterSize(1000000);
    reg.setSearchMethod(tree);
    reg.setNumberOfNeighbours(30);
    reg.setInputCloud(temp_cloud);
    //reg.setIndices (indices);
    reg.setInputNormals(cloud_normals);
    reg.setSmoothnessThreshold(5.0 / 180.0 * M_PI);
    reg.setCurvatureThreshold(1.0);

    std::vector<pcl::PointIndices> clusters;
    reg.extract(clusters);
    //pcl::PointCloud <pcl::PointXYZRGB>::Ptr colored_cloud = reg.getColoredCloud ();
    //std::cout << "Number of clusters is equal to " << clusters.size () << std::endl;
    //std::cout << "First cluster has " << clusters[0].indices.size () << " points." << endl;
    // if(clusters.size ()>=2){
    // std::cout << "Second cluster has " << clusters[1].indices.size () << " points." << endl;
    // }
    float xc, yc, zc, xct, yct, zct;
    //int counter = 0;
    int i, j, m, nop;
    float n1, n2, n3, t, t1, hos;
    hos = 1.1; //++++++++++ HIGHT OF SENSOR
               //========================================================
               //DEFINE THE MESSGA THAT I HAVE CREATED
               // my_pcl_tutorial::cent msg;
               //========================================================
               //while (counter < clusters[0].indices.size ())
    // {
    //   std::cout << clusters[0].indices[counter] << ", ";

    //pcl::PointCloud<pcl::PointXYZ>::Ptr temp_cloud3(new pcl::PointCloud<pcl::PointXYZ>);
    // pcl::PointCloud<pcl::PointXYZ>::Ptr temp_cloud4(new pcl::PointCloud<pcl::PointXYZ>);
    //===================Removing the non clusteread points (removed but Not worked Hhhh'''!)=======================================
    // pcl::ExtractIndices<pcl::PointXYZ> ex3;
    // pcl::PointIndices::Ptr inliers3(new pcl::PointIndices());
    //  pcl::PointIndices::Ptr inliers4(new pcl::PointIndices());

    //for (size_t i = 0; i < clusters.size (); ++i)  //for (size_t i = 0; i < cloud->points.size (); ++i)
    //{

    //   inliers3->indices =clusters[i].indices;
    //   counter=0;
    //   while (counter <= inliers3->indices.size ()){
    //   std::cout << clusters[0].indices[counter] << std::endl;
    //              m= clusters[i].indices[counter] ;

    //             inliers4->indices.push_back(m);
    //             counter=counter+1;
    // m=m+1;
    //         }

    //}
    // std::cout << inliers4->indices.size() << "the size "<< std::endl;
    // ex3.setInputCloud(temp_cloud);
    //ex3.setIndices(inliers4);
    // ex3.setNegative(false);
    // ex3.filter(*temp_cloud);
    //===========================================================================================================================================
    float v;
    int counter = 0;
    //v=imu->linear_acceleration.z;
    //v=-v*9;

    counter = int(v);
    counter = counter % 2;
    counter = 0;
    //counter=counter+1;

    //counter=0;
    // inliers->indices.push_back(i);
    int c1l = 0;
    int c2l = 0;
    int c3l = 0;
    float stepc[1][4];
    stepc[0][0] = 0;
    stepc[0][1] = 0;
    stepc[0][2] = 0;
    stepc[0][3] = 0;
    pcl::PointIndices::Ptr inliers(new pcl::PointIndices());
    for (size_t i = 0; i < clusters.size(); ++i) //for (size_t i = 0; i < cloud->points.size (); ++i)
    {
      pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud2(new pcl::PointCloud<pcl::PointXYZRGB>);

      inliers->indices = clusters[i].indices;

      ////////////////////////////////////////////////////////////////////
      pcl::ExtractIndices<pcl::PointXYZRGB> extract;
      extract.setInputCloud(temp_cloud);
      extract.setIndices(inliers);
      extract.setNegative(false);
      extract.filter(*temp_cloud2);
      ////////////////////////////////////////////////////////////////////

      pcl::ModelCoefficients::Ptr coefficients(new pcl::ModelCoefficients);
      pcl::PointIndices::Ptr inliers2(new pcl::PointIndices);
      // Create the segmentation object
      pcl::SACSegmentation<pcl::PointXYZRGB> seg;
      // Optional
      seg.setOptimizeCoefficients(true);
      // Mandatory
      seg.setModelType(pcl::SACMODEL_PLANE);
      seg.setMethodType(pcl::SAC_RANSAC);
      seg.setDistanceThreshold(0.01);

      seg.setInputCloud(temp_cloud2);
      seg.segment(*inliers2, *coefficients);
      n1 = coefficients->values[0] / coefficients->values[3];
      n2 = coefficients->values[1] / coefficients->values[3];
      n3 = coefficients->values[2] / coefficients->values[3];

      Eigen::Vector4f xyz_centroid;

      // Estimate the XYZ centroid
      compute3DCentroid(*temp_cloud2, xyz_centroid);
      xc = xyz_centroid[0];
      yc = xyz_centroid[1];
      zc = xyz_centroid[2];

      //==========================
      float angle = 0;
      //float angled=0;
      //angle=roll*180/3.14;
      //angle=angle+180;
      angle = angch;
      //angle=           //31.5;//==================================HERE IS THE ******
      t = atan(n3 / n2);
      t1 = atan(n3 / n1);

      t = t * 180 / 3.14; // 0->flat, 90 or -90->wall
      t1 = t1 * 180 / 3.14;

      t = t - angle;

      angle = angle * 3.14 / 180;
      //angle=0.485179;
      //angle=0.439103;
      p = 0;
      float theta = -angle; //(vc*3.14)/180;

      Eigen::MatrixXd trans(4, 4);
      Eigen::MatrixXd transa(4, 4);
      Eigen::MatrixXd transb(4, 4);
      trans << cos(theta), -sin(theta), 0.0, 0.0,
          sin(theta), cos(theta), 0.0, 0.0,
          0.0, 0.0, 1.0, 0.0,
          0.0, 0.0, 0.0, 1.0;

      transa << 1.0, 0.0, 0.0, 0.0,
          0.0, cos(theta), -sin(theta), 0.0,
          0.0, sin(theta), cos(theta), 0.0,
          0.0, 0.0, 0.0, 1.0;

      // transb << cos(theta), 0.0, sin(theta), 0.0,
      //     0.0, 1.0, 0.0, 0.0,
      //     -sin(theta), 0.0, cos(theta), 0.0,
      //     0.0, 0.0, 0.0, 1.0;

      Eigen::MatrixXd ccnt(4, 1);
      Eigen::MatrixXd rcnt(4, 1);
      ccnt << xc,
          yc,
          zc,
          1.0;

      rcnt = transa * ccnt;
      xc = rcnt(0, 0);
      yc = rcnt(1, 0);
      zc = rcnt(2, 0);

      //==========================

      //std::cerr << zc <<"zc" << std::endl;
      // Compute the 3x3 covariance matrix
      //computeCovarianceMatrix (cloud, xyz_centroid, covariance_matrix);
      nop = 200; //clusters[i].indices.size();
      yc = -(yc - hos);

      //std::cerr << i <<"  Cluster" << std::endl;
      //std::cerr << t <<"  Normal" << std::endl;
      //std::cerr << zc <<"  zc" << std::endl;

      // std::cerr << v <<"  v" << std::endl;

      //=============Debegging part====================
      //  std::cerr << "" <<"  " << std::endl;
      //std::cerr << "Cluster" << i << " "
      //                               "yc"
      ////          << yc << "  "
      //                  //          "angle:"    << angch << "  "
      //                  "zc:"
      //         << zc << "  "
      //                  "t="
      //        << t << "  " << std::endl;

      //"Filtered out:"  << yc << " " <<
      //====================================
      if (t < 40 && t > -40 && (t1 > 70 || t1 < -70)) //&& yc <= 0.1 && yc >= -0.1
      {                      ///=============GROUND(p<10 && p>-10)
        // msg.tg=1;
        //  msg.xg=xc;
        //   msg.yg=yc;
        //    msg.zg=zc;

        //std::cerr << xc <<" " << yc <<" " <<zc <<" " << t <<" "<<std::endl;
        //std::cerr << yc <<"  yc" << std::endl;
        //std::cerr << v <<"  Angle" << std::endl;

        //usleep(1000);//========================wait()>>>
        //std::cerr << xc <<"  xc" << std::endl;

        //std::cerr << t <<"  t " << std::endl;
        ros::NodeHandle nh;
        ros::ServiceClient client = nh.serviceClient<terrain_detection::Classifier>("classifier");
        terrain_detection::Classifier srv;
        srv.request.a = xc;
        srv.request.b = yc;
        srv.request.c = zc;
        srv.request.d = t;
        float terr = 0;
        //std::cerr << yc << "  yc" << std::endl;
        if (client.call(srv))
        {
          terr = srv.response.result;
          std::cerr << "terr=" << terr << std::endl;
          if (terr == 1)
          {
            for (size_t j = 0; j < inliers->indices.size(); ++j)
            {
              temp_cloud->points[clusters[i].indices[j]].r = 255;
              temp_cloud->points[clusters[i].indices[j]].g = 255;
              temp_cloud->points[clusters[i].indices[j]].b = 0;
            }
          }
          else if (terr == 2)
          {
            for (size_t j = 0; j < inliers->indices.size(); ++j)
            {
              temp_cloud->points[clusters[i].indices[j]].r = 100;
              temp_cloud->points[clusters[i].indices[j]].g = 0;
              temp_cloud->points[clusters[i].indices[j]].b = 100;
            }
          }
          else if (terr == 3)
          {
            for (size_t j = 0; j < inliers->indices.size(); ++j)
            {
              temp_cloud->points[clusters[i].indices[j]].r = 0;
              temp_cloud->points[clusters[i].indices[j]].g = 200;
              temp_cloud->points[clusters[i].indices[j]].b = 0;
            }
          }
          else if (terr == 4)
          {
            for (size_t j = 0; j < inliers->indices.size(); ++j)
            {
              temp_cloud->points[clusters[i].indices[j]].r = 200;
              temp_cloud->points[clusters[i].indices[j]].g = 0;
              temp_cloud->points[clusters[i].indices[j]].b = 0;
            }
          }
          else if (terr == 5)
          {
            for (size_t j = 0; j < inliers->indices.size(); ++j)
            {
              temp_cloud->points[clusters[i].indices[j]].r = 0;
              temp_cloud->points[clusters[i].indices[j]].g = 0;
              temp_cloud->points[clusters[i].indices[j]].b = 200;
            }
          }
        }
        //else
        //{
        // ROS_ERROR("Failed to call service add_two_ints");
        //}

        //ros::ServiceClient client = nh.serviceClient<pythonode::AddTwoInts>("add_two_ints");
        //pythonode::AddTwoInts srv;
        //srv.request.a = 5;
        //srv.request.b = 5;
        //yc = srv.response.sum;
        //std::cerr << yc << "  yc" << std::endl;
        //if (client.call(srv))
        //{
        //  ROS_INFO("Sum: %ld", (long int)srv.response.sum);
        //}
        //else
        //{
        //  ROS_ERROR("Failed to call service add_two_ints");
        //}
      }
    }
  }
  //publishing the data
  pcl::PCLPointCloud2 cloudB;
  pcl::toPCLPointCloud2(*temp_cloud, cloudB);

  // Convert to ROS data type
  sensor_msgs::PointCloud2 output;
  pcl_conversions::moveFromPCL(cloudB, output);
  //output.Transform=input.Transform;

  //for (size_t i = 0; i < output->points.size (); ++i){}

  pub.publish(output);
}

int main(int argc, char **argv)
{

  // Initialize ROS
  ros::init(argc, argv, "mya");
  ros::NodeHandle nh;

  //cout<<"hello";
  // Create a ROS subscriber for the input point cloud
  //ros::Subscriber sub = nh.subscribe ("cdsac", 1, cloud_cb); //dsample   /camera/depth/points

  message_filters::Subscriber<sensor_msgs::PointCloud2> pc_sub(nh, "cdsac", 1);
  message_filters::Subscriber<sensor_msgs::Imu> imu_sub(nh, "imu/data", 1); //imu
  typedef sync_policies::ApproximateTime<PointCloud2, Imu> MySyncPolicy;
  // ApproximateTime takes a queue size as its constructor argument, hence MySyncPolicy(10)
  Synchronizer<MySyncPolicy> sync(MySyncPolicy(40), pc_sub, imu_sub);
  sync.registerCallback(boost::bind(&cloud_cb, _1, _2));

  // Create a ROS publisher for the output point cloud
  pub = nh.advertise<sensor_msgs::PointCloud2>("mya", 1);
  pubm = nh.advertise<terrain_detection::cent>("TP", 1);

  // Spin
  ros::spin();
}
