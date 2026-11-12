
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

#include <std_msgs/Float32.h>




using namespace sensor_msgs;
using namespace message_filters;
using namespace std_msgs;

ros::Publisher pub;
ros::Publisher pubm;

int cal = 5;
int cal_time = cal;
bool cal_state = true;

float offset=0.0;//-1; //(minus more downramp) 1.2 is the calb value
float hos =1.1 , hos_av = 0;
float Step_size=0.5;

bool ds, ups,stps_update;
bool cover_step1 = false;
bool cover_step2 = false;
bool cover_step3 = false;


class clouds
{
public:
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr s1;
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr s2;
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr s3;
    int cloud_st;
};

class cloud_feature
{ 
public:
   pcl::PointCloud<pcl::PointXYZRGB>::Ptr point_cloud;
   std::vector<std::vector<float> > features_matrix;
};
//struct clouds;

void cloud_cb(const boost::shared_ptr<const sensor_msgs::PointCloud2> &input, const sensor_msgs::Imu::ConstPtr &imu)
{
    ups = false;
    ds = false;

    //IMU processing
    float roll = 0, angle = 0;
    double r, p, y;
    tf::Quaternion quat;
    tf::quaternionMsgToTF(imu->orientation, quat);
    tf::Matrix3x3(quat).getRPY(r, p, y);
    roll = r;
    p = p * 180 / 3.14;
    angle = (roll * 180 / 3.14) + 180;
    //std::cerr << "angch= " << angch << std::endl;
    
    //Point cloud covnersion to pcl type
    pcl::PCLPointCloud2 pcl_pc2;
    pcl_conversions::toPCL(*input, pcl_pc2);
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud(new pcl::PointCloud<pcl::PointXYZRGB>);
    pcl::fromPCLPointCloud2(pcl_pc2, *temp_cloud);

    //Height of Sensor and Calabration================

    float angle_cal;
    angle_cal = (angle - 90) * -1;

    extern float calabration(pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud, float angle);

    if (cal_state == false)
    {
        hos = calabration(temp_cloud, angle_cal);
        if (hos > 0)
        {
            std::cerr << "calabrating.. " << cal << std::endl;
            usleep(100000);
            cal = cal - 1;
            hos_av = hos_av + hos;
        }
        else
        {
            cal = 5;
            hos_av = 0;
        }
        if (cal == 0)
        {
            hos_av = hos_av / cal_time;
            std::cerr << "hos=" << hos_av << std::endl;
            hos = hos_av;
            cal_state = true;
        }
    }

    //===================================================

    //std::cerr << "hos= " << hos << std::endl;

    //Defining the needed functions for the detection
    extern pcl::PointCloud<pcl::PointXYZRGB>::Ptr cloud_process(pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud, float angle, float hos);
    //Detect only with certin ranges
    if (angle <= 180 && angle >= 0 && cal_state == true && temp_cloud->points.size()>=50)
    {
        angle = (angle-90) * -1;
        
        //===cloud sepration=========

        extern clouds cloud_speration(pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud);
        clouds s_cloud;
        s_cloud = cloud_speration(temp_cloud);
        // std::cerr << "s_cloud= " << s_cloud.cloud_st << std::endl;

        float tc1 = 0, tc2 = 0, tc3 = 0, dif1, dif2;
        float DifThr = 5;
        extern float g_normal(pcl::PointCloud<pcl::PointXYZRGB>::Ptr input_cloud);

        extern cloud_feature cloud_process(pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud, float angle, float hos);
        extern std::vector<std::vector<float> > arrange_matrix(std::vector<std::vector<float> > input1,std::vector<std::vector<float> > input2);
        
        cloud_feature tcloud_features;
        std::vector<std::vector<float> > output;
        cloud_feature tclouds1_features;
        std::vector<std::vector<float> > output1;
        cloud_feature tclouds2_features;
        std::vector<std::vector<float> > output2;
        cloud_feature tclouds3_features;
        std::vector<std::vector<float> > output3;
         




        if (s_cloud.cloud_st == 123)
        {   
            tcloud_features=cloud_process(temp_cloud, angle, hos);
            temp_cloud=tcloud_features.point_cloud;
            output=tcloud_features.features_matrix;
        }
        else if (s_cloud.cloud_st == 23)
        {   
            tc1 = g_normal(s_cloud.s1);
            tc2 = g_normal(s_cloud.s2);
            dif1 = abs(tc1 - tc2);
            if (dif1 < DifThr)
            {   
                tcloud_features=cloud_process(temp_cloud, angle, hos);
                temp_cloud=tcloud_features.point_cloud;
                output=tcloud_features.features_matrix;
            }
            else
            {   
                //s_cloud.s1 = cloud_process(s_cloud.s1, angle, hos);
                //s_cloud.s2 = cloud_process(s_cloud.s2, angle, hos);
                //*temp_cloud = *s_cloud.s1 + *s_cloud.s2;
                
                
                tclouds1_features=cloud_process(s_cloud.s1, angle, hos);
                tclouds2_features=cloud_process(s_cloud.s2, angle, hos);
                
                *temp_cloud=*tclouds1_features.point_cloud + *tclouds2_features.point_cloud;
                
                tcloud_features.point_cloud=temp_cloud;
                

                output1=tclouds1_features.features_matrix;
                output2=tclouds2_features.features_matrix;
                tcloud_features.features_matrix=arrange_matrix(output1,output2);
                output=tcloud_features.features_matrix;
            }
        }
        else
        {   
            tc1 = g_normal(s_cloud.s1);
            tc2 = g_normal(s_cloud.s2);
            tc3 = g_normal(s_cloud.s3);
            dif1 = abs(tc1 - tc2);
            dif2 = abs(tc2 - tc3);
            if (dif1 < DifThr && dif2 < DifThr)
            {   
                //temp_cloud = cloud_process(temp_cloud, angle, hos);
                tcloud_features=cloud_process(temp_cloud, angle, hos);
                temp_cloud=tcloud_features.point_cloud;
                output=tcloud_features.features_matrix;
            }
            else if (dif1 >= DifThr && dif2 < DifThr)
            {
               //*s_cloud.s2 = *s_cloud.s2 + *s_cloud.s3;
               // s_cloud.s1 = cloud_process(s_cloud.s1, angle, hos);
               // s_cloud.s2 = cloud_process(s_cloud.s2, angle, hos);
               // *temp_cloud = *s_cloud.s1 + *s_cloud.s2;
                
                *s_cloud.s2 = *s_cloud.s2 + *s_cloud.s3;
                tclouds1_features=cloud_process(s_cloud.s1, angle, hos);
                tclouds2_features=cloud_process(s_cloud.s2, angle, hos);
                *temp_cloud= *tclouds1_features.point_cloud + *tclouds2_features.point_cloud;
                tcloud_features.point_cloud=temp_cloud;

                output1=tclouds1_features.features_matrix;
                output2=tclouds2_features.features_matrix;
                tcloud_features.features_matrix=arrange_matrix(output1,output2);
                output=tcloud_features.features_matrix;

            }
            else if (dif1 < DifThr && dif2 >= DifThr)
            {
                //*s_cloud.s1 = *s_cloud.s1 + *s_cloud.s2;
                //s_cloud.s1 = cloud_process(s_cloud.s1, angle, hos);
                //s_cloud.s3 = cloud_process(s_cloud.s3, angle, hos);
                //*temp_cloud = *s_cloud.s1 + *s_cloud.s3;
                
                *s_cloud.s1 = *s_cloud.s1 + *s_cloud.s2;
                tclouds1_features=cloud_process(s_cloud.s1, angle, hos);
                tclouds3_features=cloud_process(s_cloud.s3, angle, hos);
                
                *temp_cloud= *tclouds1_features.point_cloud + *tclouds3_features.point_cloud;
               
                tcloud_features.point_cloud=temp_cloud;
                

                output1=tclouds1_features.features_matrix;
                output3=tclouds3_features.features_matrix;
                tcloud_features.features_matrix=arrange_matrix(output1,output3);
                output=tcloud_features.features_matrix;
            }
            else if (dif1 >= DifThr && dif2 >= DifThr)
            {
                //s_cloud.s1 = cloud_process(s_cloud.s1, angle, hos);
                //s_cloud.s2 = cloud_process(s_cloud.s2, angle, hos);
                //s_cloud.s3 = cloud_process(s_cloud.s3, angle, hos);
                //*s_cloud.s1 = *s_cloud.s1 + *s_cloud.s2;
                //*temp_cloud = *s_cloud.s1 + *s_cloud.s3;
                
                tclouds1_features=cloud_process(s_cloud.s1, angle, hos);
                tclouds2_features=cloud_process(s_cloud.s2, angle, hos);
                tclouds3_features=cloud_process(s_cloud.s3, angle, hos);
                *s_cloud.s1= *tclouds1_features.point_cloud + *tclouds2_features.point_cloud;
                *temp_cloud=*s_cloud.s1 + *tclouds3_features.point_cloud; //s_cloud.s1 just a storge
                tcloud_features.point_cloud=temp_cloud;

                output1=tclouds1_features.features_matrix;
                output2=tclouds2_features.features_matrix;
                output3=tclouds3_features.features_matrix;
                output1=arrange_matrix(output1,output2);
                tcloud_features.features_matrix=arrange_matrix(output1,output3);
                output=tcloud_features.features_matrix;
            }
        } 

        //=================================================
        //std::cerr <<"START ="<< std::endl;
        // for (int i = 0; i < output.size(); i++){
        //std::cerr <<output[i][0] <<"  "<<output[i][1] <<"  "<<output[i][2] <<"  "<<output[i][3] <<"  "<<output[i][4] <<"  "<<output[i][5] <<"  "<<output[i][6] <<"  "<<output[i][7] <<"  "<< std::endl;
        //}
        //std::cerr <<"END "<< std::endl; 
        
       
      
        //FEED THESE IN CASE OF SUCESS CODE TESTING TO THE CLOUD MERAGE AND SPLIT ....... 
        //Combine all to gother and feed them to the terrain P function.
        extern void twf(cloud_feature input);
        twf(tcloud_features);
        //==================================================
    }

    // Convert point cloud to ROS data type
    pcl::PCLPointCloud2 cloudB;
    pcl::toPCLPointCloud2(*temp_cloud, cloudB);
    sensor_msgs::PointCloud2 output;
    pcl_conversions::moveFromPCL(cloudB, output);
    //output.Transform=input.Transform;
    //for (size_t i = 0; i < output->points.size (); ++i){}
    //publishing the data
    pub.publish(output);
}

void step_cb(std_msgs::Float32 msg)
{ float x;
  x=msg.data;
  //std::cerr << "step_size=" <<x << std::endl;
  if(x>0){
  Step_size=x;
  }else{
  Step_size=0.5;
  }
  stps_update=true;
  
}


int main(int argc, char **argv)
{

    // Initialize ROS
    ros::init(argc, argv, "mya");
    ros::NodeHandle nh;

    //cout<<"hello";
    // Create a ROS subscriber for the input point cloud
    ros::Subscriber sub = nh.subscribe ("step_size", 1, step_cb); //dsample   /camera/depth/points

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

clouds cloud_speration(pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud)
{
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr s1_cloud(new pcl::PointCloud<pcl::PointXYZRGB>);
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr s2_cloud(new pcl::PointCloud<pcl::PointXYZRGB>);
    pcl::PointCloud<pcl::PointXYZRGB>::Ptr s3_cloud(new pcl::PointCloud<pcl::PointXYZRGB>);

    pcl::PointIndices::Ptr inliers(new pcl::PointIndices());
    pcl::PointIndices::Ptr inliers1(new pcl::PointIndices());
    pcl::PointIndices::Ptr inliers2(new pcl::PointIndices());
    pcl::PointIndices::Ptr inliers3(new pcl::PointIndices());

    pcl::ExtractIndices<pcl::PointXYZRGB> extract;

    for (size_t i = 0; i < temp_cloud->points.size(); ++i)
    {

        if (i < 600) //|| (zcr > 1.6 && zcr<=2.2)||(zcr > 2.3)
        {            //(zcr<=1.5) || (zcr>1.6 && zcr<=2.3) || (zcr>2.4)
            inliers1->indices.push_back(i);
        }
        else if (i >= 600 && i <= 1500)
        {
            inliers2->indices.push_back(i);
        }
        else
        {
            inliers3->indices.push_back(i);
        }
    }

    //std::cout << "sizein: \n " << temp_cloud->points.size () << std::endl;

    extract.setInputCloud(temp_cloud);
    extract.setIndices(inliers1);
    extract.setNegative(false); //TRUE
    extract.filter(*s1_cloud);

    extract.setInputCloud(temp_cloud);
    extract.setIndices(inliers2);
    extract.setNegative(false); //TRUE
    extract.filter(*s2_cloud);

    extract.setInputCloud(temp_cloud);
    extract.setIndices(inliers3);
    extract.setNegative(false); //TRUE
    extract.filter(*s3_cloud);

    clouds Cloud;
    //Cloud.cloud_st=10;

    Cloud.s1 = s1_cloud;
    Cloud.s2 = s2_cloud;
    Cloud.s3 = s3_cloud;

    if (s2_cloud->points.size() < 500 || s1_cloud->points.size() < 500)
    {

        *s1_cloud = *s1_cloud + *s2_cloud;
        *s1_cloud = *s1_cloud + *s3_cloud;
        Cloud.s1 = s1_cloud;
        Cloud.cloud_st = 123;
    }
    else if (s3_cloud->points.size() < 500)
    {

        *s2_cloud = *s2_cloud + *s3_cloud;
        Cloud.s2 = s2_cloud;
        Cloud.cloud_st = 23;
    }
    else
    {
        Cloud.cloud_st = 0;
    }

    return Cloud;
}

cloud_feature cloud_process(pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud, float angle, float hos)
{
    //Normal Estimation process
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
    // Finding the normals
    ne.compute(*cloud_normals);

    //Regional growing process for clusters
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

    //Centriod parameters
    float xc, yc, zc, xct, yct, zct;
    int i, j, m, nop, cl, acl = 0;
    float n1, n2, n3, t, t1;
    cl = clusters.size();
    if (cl == 0)
    {
        cl = 1;
    }
    //Treat each cluster seperatly plan fitting, feature transformation.....
    pcl::PointIndices::Ptr inliers(new pcl::PointIndices());

    float yc_ground = 0;
    float f_matrix[cl][7], tm[1][7];
    

    for (size_t i = 0; i < clusters.size(); ++i)
    {

        //extract the clusters points and save them in temp_cloud2
        pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud2(new pcl::PointCloud<pcl::PointXYZRGB>);
        inliers->indices = clusters[i].indices;
        ////////////////////////////////////////////////////////////////////
        pcl::ExtractIndices<pcl::PointXYZRGB> extract;
        extract.setInputCloud(temp_cloud);
        extract.setIndices(inliers);
        extract.setNegative(false);
        extract.filter(*temp_cloud2);
        ////////////////////////////////////////////////////////////////////

        //Feature extraction(orientaion and cetriod)
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

        //Obtaining the plane coefficients
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

        t = atan(n3 / n2);
        t1 = atan(n3 / n1);

        t = t * 180 / 3.14; // 0->flat, 90 or -90->wall
        t1 = t1 * 180 / 3.14;

        t = t - angle+offset;

        float theta = -(angle * 3.14 / 180); //(vc*3.14)/180;

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

        nop = clusters[i].indices.size();
        yc = -(yc - hos);

        //=============Debegging part====================
        //std::cerr << " "
        //          << "  " << std::endl;
        /*std::cerr << "Cluster" << i << " "
                                       "yc"
                  << yc << "  "
                           "zc:"
                  << zc << "  "
                           "t="
                  << t << "  " << std::endl;*/

        //std::cerr << "Angle" <<angle << std::endl;
        //"Filtered out:"  << yc << " " <<
        //====================================

        if (t < 40 && t > -40 && (t1 > 70 || t1 < -70))
        {

            //=====Fill the feature matrix==
            f_matrix[i][0] = xc;
            f_matrix[i][1] = yc;
            f_matrix[i][2] = zc;
            f_matrix[i][3] = t;
            f_matrix[i][4] = nop;
            f_matrix[i][5] = i;
            f_matrix[i][6] = 1;
            acl = acl + 1;


        }
        else
        {
            //=====Fill the feature matrix==
            f_matrix[i][0] = xc;
            f_matrix[i][1] = yc;
            f_matrix[i][2] = zc;
            f_matrix[i][3] = t;
            f_matrix[i][4] = nop;
            f_matrix[i][5] = i;
            f_matrix[i][6] = 0;
        }
    }

    //Display the input matrix
    /*for (size_t  i= 0; i < cl; i++){
        for (size_t  j= 0; j < 5; j++){
        cout<< " \n";
        cout<< "Element_IN("<<i<<j<<")=" <<f_matrix[i][j];
        cout<< " \n";
        }
    }*/
    //==Rearrange the matrix========
    for (size_t i = 0; i < cl; i++)
    {
        for (size_t j = 0; j < cl; j++)
        {
            if (f_matrix[i][2] < f_matrix[j][2])
            {
                tm[0][0] = f_matrix[i][0];
                tm[0][1] = f_matrix[i][1];
                tm[0][2] = f_matrix[i][2];
                tm[0][3] = f_matrix[i][3];
                tm[0][4] = f_matrix[i][4];
                tm[0][5] = f_matrix[i][5];
                tm[0][6] = f_matrix[i][6];
                f_matrix[i][0] = f_matrix[j][0];
                f_matrix[i][1] = f_matrix[j][1];
                f_matrix[i][2] = f_matrix[j][2];
                f_matrix[i][3] = f_matrix[j][3];
                f_matrix[i][4] = f_matrix[j][4];
                f_matrix[i][5] = f_matrix[j][5];
                f_matrix[i][6] = f_matrix[j][6];
                f_matrix[j][0] = tm[0][0];
                f_matrix[j][1] = tm[0][1];
                f_matrix[j][2] = tm[0][2];
                f_matrix[j][3] = tm[0][3];
                f_matrix[j][4] = tm[0][4];
                f_matrix[j][5] = tm[0][5];
                f_matrix[j][6] = tm[0][6];
            }
        }
    }

    cloud_feature tcloud_feature;
    if (acl > 0) //Affordances condition if there is  
    {
        //acl=1;

        float arf_matrix[acl][8];
        int indx = 0;
        for (size_t i = 0; i < cl; i++)
        {
            if (f_matrix[i][6] == 1)
            {
                arf_matrix[indx][0] = f_matrix[i][0];
                arf_matrix[indx][1] = f_matrix[i][1];
                arf_matrix[indx][2] = f_matrix[i][2];
                arf_matrix[indx][3] = f_matrix[i][3];
                arf_matrix[indx][4] = f_matrix[i][4];
                arf_matrix[indx][5] = f_matrix[i][5];
                arf_matrix[indx][6] = 0;
                arf_matrix[indx][7] = 0;
                indx = indx + 1;
            }
        }
        
        //================================================
        

        for (size_t i = 0; i < acl; i++)
        {
            
            //if (f_matrix[i][6] ==1)
            //{
            /* code */
            float cl_i;
            cl_i = arf_matrix[i][5];
            //======MACHINE LEARNING CLASSIFIER=========================
            ros::NodeHandle nh;
            ros::ServiceClient client = nh.serviceClient<terrain_detection::Classifier>("classifier");
            terrain_detection::Classifier srv;
            //srv.request.a = arf_matrix[i][0];
            srv.request.b = arf_matrix[i][1];
            srv.request.c = arf_matrix[i][2];
            srv.request.d = arf_matrix[i][3];
            //srv.request.e = acl;
            float terr = 0;
            

            
            if (client.call(srv))
            {
                terr = srv.response.result;
                //std::cerr <<angle <<" "<<arf_matrix[i][3]<<" "<<terr<< std::endl;
                //std::cerr << "terr=" << terr << std::endl;
                //std::cerr << "angle=" << angle << std::endl;

                if (terr == 1)
                {
                    for (size_t j = 0; j < arf_matrix[i][4]; ++j)
                    {
                        temp_cloud->points[clusters[cl_i].indices[j]].r = 255;
                        temp_cloud->points[clusters[cl_i].indices[j]].g = 255;
                        temp_cloud->points[clusters[cl_i].indices[j]].b = 0;
                    }
                    ds = true;
                }
                else if (terr == 2)
                {
                    for (size_t j = 0; j < arf_matrix[i][4]; ++j)
                    {
                        temp_cloud->points[clusters[cl_i].indices[j]].r = 100;
                        temp_cloud->points[clusters[cl_i].indices[j]].g = 0;
                        temp_cloud->points[clusters[cl_i].indices[j]].b = 100;
                    }
                }
                else if (terr == 3)
                {
                    for (size_t j = 0; j < arf_matrix[i][4]; ++j)
                    {
                        temp_cloud->points[clusters[cl_i].indices[j]].r = 0;
                        temp_cloud->points[clusters[cl_i].indices[j]].g = 200;
                        temp_cloud->points[clusters[cl_i].indices[j]].b = 0;
                    }
                    //yc_ground=yc;
                }
                else if (terr == 4)
                {
                    for (size_t j = 0; j < arf_matrix[i][4]; ++j)
                    {
                        temp_cloud->points[clusters[cl_i].indices[j]].r = 200;
                        temp_cloud->points[clusters[cl_i].indices[j]].g = 0;
                        temp_cloud->points[clusters[cl_i].indices[j]].b = 0;
                    }
                }
                else if (terr == 5)
                {
                    for (size_t j = 0; j < arf_matrix[i][4]; ++j)
                    {
                        temp_cloud->points[clusters[cl_i].indices[j]].r = 0;
                        temp_cloud->points[clusters[cl_i].indices[j]].g = 0;
                        temp_cloud->points[clusters[cl_i].indices[j]].b = 200;
                    }
                    ups = true;
                }
            }
            arf_matrix[i][7]=terr;
            //}
        }

        std::vector<std::vector<float> > output(acl);
        std::vector<float> tm(8,0);
   
        for (size_t i = 0; i < acl; i++)
        {
         //output[i][1]=arf_matrix[i][1];
          tm[0] = arf_matrix[i][0];
          tm[1] = arf_matrix[i][1];
          tm[2] = arf_matrix[i][2];
          tm[3] = arf_matrix[i][3];
          tm[4] = arf_matrix[i][4];
          tm[5] = arf_matrix[i][5];
          tm[6] = arf_matrix[i][6];
          tm[7] = arf_matrix[i][7];
          output[i]=tm;
          
        }

     //     std::cerr <<"START ="<< acl<< std::endl;
     //     for (size_t i = 0; i < acl; i++){
       
     //      std::cerr <<output[i][0] <<"  "<<output[i][1] <<"  "<<output[i][2] <<"  "<<output[i][3] <<"  "<<output[i][4] <<"  "<<output[i][5] <<"  "<<output[i][6] <<"  "<<output[i][7] <<"  "<< std::endl;
     //    }
     //     std::cerr <<"END "<< std::endl;

       tcloud_feature.features_matrix=output;    
    }else
    {  std::vector<std::vector<float> > output(1);
       std::vector<float> tm(8,0);
       output[0]=tm;
       tcloud_feature.features_matrix=output;     
    }
    //==========Feature matrix===========
    tcloud_feature.point_cloud=temp_cloud;
    //===================================
    return tcloud_feature;
}

float calabration(pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud, float angle)
{
    //Normal Estimation process
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
    // Finding the normals
    ne.compute(*cloud_normals);

    //Regional growing process for clusters
    pcl::RegionGrowing<pcl::PointXYZRGB, pcl::Normal> reg;
    reg.setMinClusterSize(500);
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

    //Centriod parameters
    float xc, yc, zc, xct, yct, zct, ycal = 0;
    int i, j, m, nop;
    float n1, n2, n3, t, t1;

    //Treat each cluster seperatly plan fitting, feature transformation.....
    pcl::PointIndices::Ptr inliers(new pcl::PointIndices());
    for (size_t i = 0; i < clusters.size(); ++i)
    {

        //extract the clusters points and save them in temp_cloud2
        pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud2(new pcl::PointCloud<pcl::PointXYZRGB>);
        inliers->indices = clusters[i].indices;
        ////////////////////////////////////////////////////////////////////
        pcl::ExtractIndices<pcl::PointXYZRGB> extract;
        extract.setInputCloud(temp_cloud);
        extract.setIndices(inliers);
        extract.setNegative(false);
        extract.filter(*temp_cloud2);
        ////////////////////////////////////////////////////////////////////

        //Feature extraction(orientaion and cetriod)
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

        //Obtaining the plane coefficients
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

        t = atan(n3 / n2);
        t1 = atan(n3 / n1);

        t = t * 180 / 3.14; // 0->flat, 90 or -90->wall
        t1 = t1 * 180 / 3.14;

        t = t - angle;

        angle = angle * 3.14 / 180;

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

        if (t < 4 && t > -4) //&& yc <= 0.1 && yc >= -0.1
        {
            ycal = yc;
        }
        else
        {
            ROS_WARN("Cannot detect the ground to calabrate, return ycal=0 and recalabrate..");
            ycal = 0;
        }
    }
    return ycal;
}



std::vector<std::vector<float> > arrange_matrix(std::vector<std::vector<float> > input1,std::vector<std::vector<float> > input2)
{   
    int s1,s2,zn;
    zn=0;
    s1=input1.size();
    s2=input2.size();
    std::vector<std::vector<float> > output(s1+s2);
    
    std::vector<float> tm(8,0);

    for (int i = 0; i < output.size(); i++){ 
      
        if (i <s1)
         {
                tm[0] = input1[i][0];
                tm[1] = input1[i][1];
                tm[2] = input1[i][2];
                tm[3] = input1[i][3];
                tm[4] = input1[i][4];
                tm[5] = input1[i][5];
                tm[6] = input1[i][6];
                tm[7] = input1[i][7];
                output[i]=tm;
                if(tm[7]>0){
                    zn=zn+1;
                }

         }else{
                tm[0] = input2[i-s1][0];
                tm[1] = input2[i-s1][1];
                tm[2] = input2[i-s1][2];
                tm[3] = input2[i-s1][3];
                tm[4] = input2[i-s1][4];
                tm[5] = input2[i-s1][5];
                tm[6] = input2[i-s1][6];
                tm[7] = input2[i-s1][7];
                output[i]=tm;
                if(tm[7]>0){
                    zn=zn+1;
                }
         } 

          
    }
    std::vector<std::vector<float> > output_ez(zn);
    zn=0;
    for (int i = 0; i < output.size(); i++){     
                tm[0] = output[i][0];
                tm[1] = output[i][1];
                tm[2] = output[i][2];
                tm[3] = output[i][3];
                tm[4] = output[i][4];
                tm[5] = output[i][5];
                tm[6] = output[i][6];
                tm[7] = output[i][7];
                //std::cerr <<tm[7] <<"  "<<std::endl;
                if(tm[7]>0){
                output_ez[zn]=tm;
                zn=zn+1;
                }
    }
    return output_ez;
} 

float g_normal(pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud2)
{
    float t, t1, xc, yc, zc, n1, n2, n3;
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

    t = atan(n3 / n2);
    t1 = atan(n3 / n1);

    t = t * 180 / 3.14; // 0->flat, 90 or -90->wall
    return t;
}

//terrain_detection::cent msg1; 
//terrain_detection::cent msg2; 
//terrain_detection::cent msg3; 
//int mc=0;
void twf(cloud_feature input)
{   pcl::PointCloud<pcl::PointXYZRGB>::Ptr temp_cloud(new pcl::PointCloud<pcl::PointXYZRGB>);
    temp_cloud=input.point_cloud;
    std::vector<std::vector<float> > features;
    features=input.features_matrix;
    terrain_detection::cent msg; 

    float first_limit, second_limt, third_limit, fourth_limit;
    //ups=false;
    //ds=false;
    //NEEDS more work 
    if(ups==true || ds==true){
    //DEFINE THE MESSGA THAT I HAVE CREATED
    //filling the features
    for (int i = 0; i < features.size(); i++){
    if(i==0 ){
    if(features[0][7]==5 || features[0][7]==1){        
    msg.yc1=features[i][1];
    //msg.tc1=features[i][3];
    msg.TDL1=features[i][7];
    msg.step1=true;
    }else{
    msg.yc1=0;
    msg.tc1=features[i][3];
    msg.TDL1=features[i][7];    
    }
    }
    if(i==1){
    msg.yc2=features[1][1]-features[0][1];
    if(features[1][7]==5 || features[1][7]==1){
    msg.yc1=features[1][1]-features[0][1];
    msg.TDL2=features[1][7];   
    msg.step2=true;
    }else{
    msg.TDL2=features[i][7];   
    msg.step2=true;
    if( msg.TDL2=features[1][7]==3 && features[1][4]>features[0][4]){
    msg.TDL1=3;//features[i][7]; 
    msg.TDL2=3;//features[i][7]; 
    msg.tc2=features[1][3];
    msg.tc1=features[1][3];
    msg.yc1=0;
    msg.yc2=0;

    }
    }
   
    }
    if(i==2){
    msg.yc3=features[1][1]-features[0][1];
    //msg.tc3=features[i][3]; 
    msg.TDL3=features[i][7];
    msg.step3=true;   
    }
    }   

    }else{
    if(stps_update==false){
    Step_size=0.5;    
    }
    std::cerr << "Step_size=" <<Step_size << std::endl;
    first_limit = Step_size;
    second_limt = first_limit - Step_size;
    third_limit = second_limt - Step_size;
    fourth_limit= third_limit- Step_size;
    //DEFINE THE MESSGA THAT I HAVE CREATED
    
    float grd1 = 0, slp1 = 0, step1 = 0, nom1 = 0, obst1 = 0, dslp1 = 0, dstep1 = 0;
    float grd2 = 0, slp2 = 0, step2 = 0, nom2 = 0, obst2 = 0, dslp2 = 0, dstep2 = 0;
    float grd3 = 0, slp3 = 0, step3 = 0, nom3 = 0, obst3 = 0, dslp3 = 0, dstep3 = 0;
    float grd4 = 0, slp4 = 0, step4 = 0, nom4 = 0, obst4 = 0, dslp4 = 0, dstep4 = 0;
    float zs = 0, k = 0, ys = 0;
    int xct = 0;
    int nom0=10;
    for (size_t k = 0; k < temp_cloud->points.size(); k++) //for (size_t i = 0; i < cloud->points.size (); ++i)
    { //zs = temp_cloud->points[k].z;
      ys = temp_cloud->points[k].y;
      zs = ys;
      if (zs <= first_limit && zs > second_limt)
        {
            nom1 = nom1 + 1;

            if (temp_cloud->points[k].r == 0 && temp_cloud->points[k].g == 200 && temp_cloud->points[k].b == 0)
            {
                grd1 = grd1 + 1;
            }
            else if (temp_cloud->points[k].r == 200 && temp_cloud->points[k].g == 0 && temp_cloud->points[k].b == 0)
            {
                slp1 = slp1 + 1;
            }
            else if ((temp_cloud->points[k].r == 0 && temp_cloud->points[k].g == 0 && temp_cloud->points[k].b == 200))
            {
                step1 = step1 + 1;
            }
            else if ((temp_cloud->points[k].r == 100 && temp_cloud->points[k].g == 0 && temp_cloud->points[k].b == 100))
            {
                dslp1 = dslp1 + 1;
            }
            else if ((temp_cloud->points[k].r == 255 && temp_cloud->points[k].g == 255 && temp_cloud->points[k].b == 0))
            {
                dstep1 = dstep1 + 1;
            }
            else
            {
                obst1 = obst1 + 1;
            }

            if (nom1 > nom0)
            {
                msg.step1 = true;
            }else{
                msg.step1 = false;
            }

            if (cover_step1 == true)
            {
                temp_cloud->points[k].r = 0;
                temp_cloud->points[k].g = 0;
                temp_cloud->points[k].b = 0;
            }
        }

        if ((zs > third_limit && zs <= second_limt))
        {
            nom2 = nom2 + 1;
            if (temp_cloud->points[k].r == 0 && temp_cloud->points[k].g == 200 && temp_cloud->points[k].b == 0)
            {
                grd2 = grd2 + 1;
            }
            else if (temp_cloud->points[k].r == 200 && temp_cloud->points[k].g == 0 && temp_cloud->points[k].b == 0)
            {
                slp2 = slp2 + 1;
            }
            else if (temp_cloud->points[k].r == 0 && temp_cloud->points[k].g == 0 && temp_cloud->points[k].b == 200)
            {
                step2 = step2 + 1;
            }
            else if ((temp_cloud->points[k].r == 100 && temp_cloud->points[k].g == 0 && temp_cloud->points[k].b == 100))
            {
                dslp2 = dslp2 + 1;
            }
            else if ((temp_cloud->points[k].r == 255 && temp_cloud->points[k].g == 255 && temp_cloud->points[k].b == 0))
            {
                dstep2 = dstep2 + 1;
            }
            else
            {
                obst2 = obst2 + 1;
            }

            if (nom2 > nom0)
            {
                msg.step2 = true;
            }else{
                msg.step2 = false;
            }

            if (cover_step2 == true)
            {
                temp_cloud->points[k].r = 0;
                temp_cloud->points[k].g = 0;
                temp_cloud->points[k].b = 0;
            }
        }

        if ((zs <= third_limit))
        {
            nom3 = nom3 + 1;
            if (temp_cloud->points[k].r == 0 && temp_cloud->points[k].g == 200 && temp_cloud->points[k].b == 0)
            {
                grd3 = grd3 + 1;
            }
            else if (temp_cloud->points[k].r == 200 && temp_cloud->points[k].g == 0 && temp_cloud->points[k].b == 0)
            {
                slp3 = slp3 + 1;
            }
            else if ((temp_cloud->points[k].r == 0 && temp_cloud->points[k].g == 0 && temp_cloud->points[k].b == 200))
            {
                step3 = step3 + 1;
            }
            else if ((temp_cloud->points[k].r == 100 && temp_cloud->points[k].g == 0 && temp_cloud->points[k].b == 100))
            {
                dslp3 = dslp3 + 1;
            }
            else if ((temp_cloud->points[k].r == 255 && temp_cloud->points[k].g == 255 && temp_cloud->points[k].b == 0))
            {
                dstep3 = dstep3 + 1;
            }
            else
            {
                obst3 = obst3 + 1;
            }

            if (nom3 > nom0)
            {
                msg.step3 = true;
            }else{
                 msg.step3 = false;
            }

            if (cover_step3 == true)
            {
                temp_cloud->points[k].r = 0;
                temp_cloud->points[k].g = 0;
                temp_cloud->points[k].b = 0;
            }
        }
    }
    extern int TDL_f(int a1, int a2, int a3, int a4, int a5);
    //========STEP ONE=======
    msg.data1[0] = int((grd1 / nom1) * 100);
    msg.data1[1] = int((slp1 / nom1) * 100);
    msg.data1[2] = int((step1 / nom1) * 100);
    msg.data1[3] = int((obst1 / nom1) * 100);
    msg.data1[4] = int((dslp1 / nom1) * 100);
    msg.data1[5] = int((dstep1 / nom1) * 100);
    //=======================
    msg.TDL1 = TDL_f(msg.data1[0], msg.data1[1], msg.data1[2], msg.data1[4], msg.data1[5]);
    //std::cout << "TDL= " << TDL_f(msg.data1[0],msg.data1[1],msg.data1[2],msg.data1[4],msg.data1[5])<< "\n";
    //========STEP TWO=======
    msg.data2[0] = int((grd2 / nom2) * 100);
    msg.data2[1] = int((slp2 / nom2) * 100);
    msg.data2[2] = int((step2 / nom2) * 100);
    msg.data2[3] = int((obst2 / nom2) * 100);
    msg.data2[4] = int((dslp2 / nom2) * 100);
    msg.data2[5] = int((dstep2 / nom2) * 100);
    //=======================
    msg.TDL2 = TDL_f(msg.data2[0], msg.data2[1], msg.data2[2], msg.data2[4], msg.data2[5]);

    //========STEP THREE=======
    msg.data3[0] = int((grd3 / nom3) * 100);
    msg.data3[1] = int((slp3 / nom3) * 100);
    msg.data3[2] = int((step3 / nom3) * 100);
    msg.data3[3] = int((obst3 / nom3) * 100);
    msg.data3[4] = int((dslp3 / nom3) * 100);
    msg.data3[5] = int((dstep3 / nom3) * 100);
    //=======================
    msg.TDL3 = TDL_f(msg.data3[0], msg.data3[1], msg.data3[2], msg.data3[4], msg.data3[5]);

    //========STEP FOUR=======
    msg.step4 = false;
    // msg.data4[0] = int((grd4 / nom4) * 100);
    // msg.data4[1] = int((slp4 / nom4) * 100);
    // msg.data4[2] = int((step4 / nom4) * 100);
    // msg.data4[3] = int((obst4 / nom4) * 100);
    // msg.data4[4] = int((dslp4 / nom4) * 100);
    //  msg.data4[5] = int((dstep4 / nom4) * 100);
    //=======================

    //filling the features
    for (int i = 0; i < features.size(); i++){
    if(msg.TDL1==features[i][7]){    
    //msg.yc1=features[i][1];
    msg.tc1=features[i][3];
    //msg.yc2=features[i][1];
    //msg.tc2=features[i][3]; 
    //msg.yc3=features[i][1];
    //msg.tc3=features[i][3];
    }    
    if(msg.TDL2==features[i][7]){    
    //msg.yc1=features[i][1];
    msg.tc2=features[i][3];
    //msg.yc2=features[i][1];
    //msg.tc2=features[i][3]; 
    //msg.yc3=features[i][1];
    //msg.tc3=features[i][3];
    }
    if(msg.TDL3==features[i][7]){    
    //msg.yc1=features[i][1];
    msg.tc3=features[i][3];
    //msg.yc2=features[i][1];
    //msg.tc2=features[i][3]; 
    //msg.yc3=features[i][1];
    //msg.tc3=features[i][3];
    }

    // if(i==0){    
    // //msg.yc1=features[i][1];
    // msg.tc1=features[i][3];
    // //msg.yc2=features[i][1];
    // msg.tc2=features[i][3]; 
    // //msg.yc3=features[i][1];
    // msg.tc3=features[i][3];
    // }
    // if(i==1){
    // //msg.yc2=features[i][1];
    // msg.tc2=features[i][3]; 
    // msg.tc3=features[i][3];   
    // }
    // if(i==2){
    // //msg.yc3=features[i][1];
    // msg.tc3=features[i][3];    
    // }
    }
    }
    pubm.publish(msg);
    //median filter processing
    // mc=mc+1;
    // if(mc==1)
    // {
    //  msg1=msg;   
    // }else if(mc==2){
    //  msg2=msg;
    // }else if(mc==3){
    //  msg3=msg; 
    //  pubm.publish(msg); 
    //  mc=0;  
    // }

    
}

int TDL_f(int a1, int a2, int a3, int a4, int a5)
{
    int matrik[5] = {a1, a2, a3, a4, a5};
    int D = 0;
    //std::cout << "Max element location: " << std::distance(matrik, std::max_element(matrik, matrik + sizeof(matrik)/sizeof(matrik[0]))) << "\n";
    D = std::distance(matrik, std::max_element(matrik, matrik + sizeof(matrik) / sizeof(matrik[0])));
    if (a1 == 0 && a2 == 0 && a3 == 0 && a4 == 0 && a5 == 0)
    {
        return 0;
    }
    else if (D == 0)
    {
        return 3;
    }
    else if (D == 1)
    {
        return 4;
    }
    else if (D == 2)
    {

        return 5;
    }
    else if (D == 3)
    {
        return 2;
    }
    else if (D == 4)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}