<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="18008000">
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
		<Item Name="callpb_photo.vi" Type="VI" URL="../callpb_photo.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="blobFromImage.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/dnn/blobFromImage.vi"/>
				<Item Name="Close File+.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Close File+.vi"/>
				<Item Name="compatReadText.vi" Type="VI" URL="/&lt;vilib&gt;/_oldvers/_oldvers.llb/compatReadText.vi"/>
				<Item Name="Create_Mat.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/Mat/Create_Mat.vi"/>
				<Item Name="Create_Mat_32F.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/Mat/Create_Mat_32F.vi"/>
				<Item Name="cvtColor.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/imgproc/cvtColor.vi"/>
				<Item Name="Find First Error.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Find First Error.vi"/>
				<Item Name="forward.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/dnn/Net/forward.vi"/>
				<Item Name="imread.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/imgcodecs/imread.vi"/>
				<Item Name="Mat_8U.lvclass" Type="LVClass" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/Mat/Mat_8U/Mat_8U.lvclass"/>
				<Item Name="Mat_32F.lvclass" Type="LVClass" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/Mat/Mat_32F/Mat_32F.lvclass"/>
				<Item Name="Mat_length.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/Mat/Mat/Mat_length.vi"/>
				<Item Name="Mat_release.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/Mat/Mat/Mat_release.vi"/>
				<Item Name="Open File+.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Open File+.vi"/>
				<Item Name="Read Delimited Spreadsheet (DBL).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Delimited Spreadsheet (DBL).vi"/>
				<Item Name="Read Delimited Spreadsheet (I64).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Delimited Spreadsheet (I64).vi"/>
				<Item Name="Read Delimited Spreadsheet (string).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Delimited Spreadsheet (string).vi"/>
				<Item Name="Read Delimited Spreadsheet.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Delimited Spreadsheet.vi"/>
				<Item Name="Read File+ (string).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read File+ (string).vi"/>
				<Item Name="Read Lines From File (with error IO).vi" Type="VI" URL="/&lt;vilib&gt;/Utility/file.llb/Read Lines From File (with error IO).vi"/>
				<Item Name="readNetFromTensorflow.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/dnn/Net/readNetFromTensorflow.vi"/>
				<Item Name="Release.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/Release.vi"/>
				<Item Name="release.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/dnn/Net/release.vi"/>
				<Item Name="scalar3.ctl" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/ctls/scalar3.ctl"/>
				<Item Name="setInput.vi" Type="VI" URL="/&lt;vilib&gt;/addons/VIRobotics/opencv_yiku/dnn/Net/setInput.vi"/>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
