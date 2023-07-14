<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="22308000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="deeplabv3_opencv.vi" Type="VI" URL="../deeplabv3_opencv.vi"/>
		<Item Name="my_onnx_test.vi" Type="VI" URL="../my_onnx_test.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="Application Directory.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Application Directory.vi"/>
				<Item Name="blobFromImage.vi" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/dnn/blobFromImage.vi"/>
				<Item Name="Color to RGB.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/colorconv.llb/Color to RGB.vi"/>
				<Item Name="ColorConversionCodes.ctl" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/ctls/ColorConversionCodes.ctl"/>
				<Item Name="Create_Mat.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/Mat/Create_Mat.vi"/>
				<Item Name="Create_Mat_8U.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/Mat/Create_Mat_8U.vi"/>
				<Item Name="Create_Mat_32F.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/Mat/Create_Mat_32F.vi"/>
				<Item Name="cvtColor.vi" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/imgproc/cvtColor.vi"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="forward.vi" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/dnn/Net/forward.vi"/>
				<Item Name="get_Mat_channel.vi" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/Mat/Mat/get_Mat_channel.vi"/>
				<Item Name="imread.vi" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/imgcodecs/imread.vi"/>
				<Item Name="Mat_8U.lvclass" Type="LVClass" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/Mat/Mat_8U/Mat_8U.lvclass"/>
				<Item Name="Mat_32F.lvclass" Type="LVClass" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/Mat/Mat_32F/Mat_32F.lvclass"/>
				<Item Name="Mat_length.vi" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/Mat/Mat/Mat_length.vi"/>
				<Item Name="Mat_release.vi" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/Mat/Mat/Mat_release.vi"/>
				<Item Name="merge_1channel_Mats.vi" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/Mat/Mat/merge_1channel_Mats.vi"/>
				<Item Name="NI_FileType.lvlib" Type="Library" URL="/&lt;vilib&gt;/Utility/lvfile.llb/NI_FileType.lvlib"/>
				<Item Name="readNetFromONNX.vi" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/dnn/Net/readNetFromONNX.vi"/>
				<Item Name="release.vi" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/release.vi"/>
				<Item Name="release.vi" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/dnn/Net/release.vi"/>
				<Item Name="resize.vi" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/imgproc/resize.vi"/>
				<Item Name="RGB to Color.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/colorconv.llb/RGB to Color.vi"/>
				<Item Name="scalar3.ctl" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/ctls/scalar3.ctl"/>
				<Item Name="setInput.vi" Type="VI" URL="/&lt;vilib&gt;/Addons/VIRobotics/opencv_yiku/dnn/Net/setInput.vi"/>
			</Item>
			<Item Name="deeplabv3_generate_color_masks.vi" Type="VI" URL="../subVI/deeplabv3_generate_color_masks.vi"/>
			<Item Name="deeplabv3_postprocess.vi" Type="VI" URL="../subVI/deeplabv3_postprocess.vi"/>
			<Item Name="deeplabV3_preprocess.vi" Type="VI" URL="../subVI/deeplabV3_preprocess.vi"/>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
