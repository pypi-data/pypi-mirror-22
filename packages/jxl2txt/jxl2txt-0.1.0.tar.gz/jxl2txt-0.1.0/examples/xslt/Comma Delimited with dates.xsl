<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"    
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" >

<!-- (c) 2006, Trimble Navigation Limited. All rights reserved.                                -->
<!-- Permission is hereby granted to use, copy, modify, or distribute this style sheet for any -->
<!-- purpose and without fee, provided that the above copyright notice appears in all copies   -->
<!-- and that both the copyright notice and the limited warranty and restricted rights notice  -->
<!-- below appear in all supporting documentation.                                             -->

<!-- TRIMBLE NAVIGATION LIMITED PROVIDES THIS STYLE SHEET "AS IS" AND WITH ALL FAULTS.         -->
<!-- TRIMBLE NAVIGATION LIMITED SPECIFICALLY DISCLAIMS ANY IMPLIED WARRANTY OF MERCHANTABILITY -->
<!-- OR FITNESS FOR A PARTICULAR USE. TRIMBLE NAVIGATION LIMITED DOES NOT WARRANT THAT THE     -->
<!-- OPERATION OF THIS STYLE SHEET WILL BE UNINTERRUPTED OR ERROR FREE.                        -->

<xsl:output method="text" omit-xml-declaration="yes" encoding="ISO-8859-1"/>

<!-- Set the numeric display details i.e. decimal point, thousands separator etc -->
<xsl:variable name="DecPt" select="'.'"/>    <!-- Change as appropriate for US/European -->
<xsl:variable name="GroupSep" select="','"/> <!-- Change as appropriate for US/European -->
<!-- Also change decimal-separator & grouping-separator in decimal-format below 
     as appropriate for US/European output -->
<xsl:decimal-format name="Standard" 
                    decimal-separator="."
                    grouping-separator=","
                    infinity="Infinity"
                    minus-sign="-"
                    NaN="?"
                    percent="%"
                    per-mille="&#2030;"
                    zero-digit="0" 
                    digit="#" 
                    pattern-separator=";" />

<xsl:variable name="DecPl0" select="'#0'"/>
<xsl:variable name="DecPl1" select="concat('#0', $DecPt, '0')"/>
<xsl:variable name="DecPl2" select="concat('#0', $DecPt, '00')"/>
<xsl:variable name="DecPl3" select="concat('#0', $DecPt, '000')"/>
<xsl:variable name="DecPl4" select="concat('#0', $DecPt, '0000')"/>
<xsl:variable name="DecPl5" select="concat('#0', $DecPt, '00000')"/>
<xsl:variable name="DecPl8" select="concat('#0', $DecPt, '00000000')"/>

<xsl:variable name="fileExt" select="'csv'"/>

<!-- User variable definitions - Appropriate fields are displayed on the       -->
<!-- Survey Controller screen to allow the user to enter specific values       -->
<!-- which can then be used within the style sheet definition to control the   -->
<!-- output data.                                                              -->
<!--                                                                           -->
<!-- All user variables must be identified by a variable element definition    -->
<!-- named starting with 'userField' (case sensitive) followed by one or more  -->
<!-- characters uniquely identifying the user variable definition.             -->
<!--                                                                           -->
<!-- The text within the 'select' field for the user variable description      -->
<!-- references the actual user variable and uses the '|' character to         -->
<!-- separate the definition details into separate fields as follows:          -->
<!-- For all user variables the first field must be the name of the user       -->
<!-- variable itself (this is case sensitive) and the second field is the      -->
<!-- prompt that will appear on the Survey Controller screen.                  -->
<!-- The third field defines the variable type - there are four possible       -->
<!-- variable types: Double, Integer, String and StringMenu.  These variable   -->
<!-- type references are not case sensitive.                                   -->
<!-- The fields that follow the variable type change according to the type of  -->
<!-- variable as follow:                                                       -->
<!-- Double and Integer: Fourth field = optional minimum value                 -->
<!--                     Fifth field = optional maximum value                  -->
<!--   These minimum and maximum values are used by the Survey Controller for  -->
<!--   entry validation.                                                       -->
<!-- String: No further fields are needed or used.                             -->
<!-- StringMenu: Fourth field = number of menu items                           -->
<!--             Remaining fields are the actual menu items - the number of    -->
<!--             items provided must equal the specified number of menu items. -->
<!--                                                                           -->
<!-- The style sheet must also define the variable itself, named according to  -->
<!-- the definition.  The value within the 'select' field will be displayed in -->
<!-- the Survey Controller as the default value for the item.                  -->

<xsl:variable name="userField1" select="'includeAttributes|Include features and attributes for points|stringMenu|2|Yes|No'"/>
<xsl:variable name="includeAttributes" select="'Yes'"/>

<xsl:variable name="userField2" select="'includeTimeStamps|Include timestamps for points|stringMenu|2|Yes|No'"/>
<xsl:variable name="includeTimeStamps" select="'Yes'"/>

<xsl:variable name="userField3" select="'includeNotes|Include notes for points|stringMenu|2|Yes|No'"/>
<xsl:variable name="includeNotes" select="'Yes'"/>

<!-- **************************************************************** -->
<!-- Set global variables from the Environment section of JobXML file -->
<!-- **************************************************************** -->
<xsl:variable name="DistUnit"   select="/JOBFile/Environment/DisplaySettings/DistanceUnits" />
<xsl:variable name="AngleUnit"  select="/JOBFile/Environment/DisplaySettings/AngleUnits" />
<xsl:variable name="CoordOrder" select="/JOBFile/Environment/DisplaySettings/CoordinateOrder" />
<xsl:variable name="TempUnit"   select="/JOBFile/Environment/DisplaySettings/TemperatureUnits" />
<xsl:variable name="PressUnit"  select="/JOBFile/Environment/DisplaySettings/PressureUnits" />

<!-- Setup conversion factor for coordinate and distance values -->
<!-- Dist/coord values in JobXML file are always in metres -->
<xsl:variable name="DistConvFactor">
  <xsl:choose>
    <xsl:when test="$DistUnit='Metres'">1.0</xsl:when>
    <xsl:when test="$DistUnit='InternationalFeet'">3.280839895</xsl:when>
    <xsl:when test="$DistUnit='USSurveyFeet'">3.2808333333357</xsl:when>
    <xsl:otherwise>1.0</xsl:otherwise>
  </xsl:choose>
</xsl:variable>

<!-- Setup conversion factor for angular values -->
<!-- Angular values in JobXML file are always in decimal degrees -->
<xsl:variable name="AngleConvFactor">
  <xsl:choose>
    <xsl:when test="$AngleUnit='DMSDegrees'">1.0</xsl:when>
    <xsl:when test="$AngleUnit='Gons'">1.111111111111</xsl:when>
    <xsl:when test="$AngleUnit='Mils'">17.77777777777</xsl:when>
    <xsl:otherwise>1.0</xsl:otherwise>
  </xsl:choose>
</xsl:variable>

<!-- Setup boolean variable for coordinate order -->
<xsl:variable name="NECoords">
  <xsl:choose>
    <xsl:when test="$CoordOrder='North-East-Elevation'">true</xsl:when>
    <xsl:when test="$CoordOrder='X-Y-Z'">true</xsl:when>
    <xsl:otherwise>false</xsl:otherwise>
  </xsl:choose>
</xsl:variable>

<!-- Setup conversion factor for pressure values -->
<!-- Pressure values in JobXML file are always in millibars (hPa) -->
<xsl:variable name="PressConvFactor">
  <xsl:choose>
    <xsl:when test="$PressUnit='MilliBar'">1.0</xsl:when>
    <xsl:when test="$PressUnit='InchHg'">0.029529921</xsl:when>
    <xsl:when test="$PressUnit='mmHg'">0.75006</xsl:when>
    <xsl:otherwise>1.0</xsl:otherwise>
  </xsl:choose>
</xsl:variable>

<!-- Set up a variable to indicate whether there are any point        -->
<!-- descriptions assigned to any points - zero means no descriptions -->
<!-- Only need to check for number of Description1 elements since     -->
<!-- both the Description1 and Description2 elements are output if    -->
<!-- either has been defined for the point.                           -->
<xsl:variable name="nbrPtDescriptions">
  <xsl:value-of select="count(JOBFile/Reductions/Point/Description1)"/>
</xsl:variable>

<!-- **************************************************************** -->
<!-- ************************** Main Loop *************************** -->
<!-- **************************************************************** -->
<xsl:template match="/" >
  <!-- Output an initial line with the job name and distance units -->
  <xsl:value-of select="'Job:'"/>
  <xsl:value-of select="JOBFile/@jobName"/>
  <xsl:value-of select="concat(',Units:', $DistUnit)"/>
  <xsl:call-template name="NewLine"/>

  <!-- Select Reductions node to process -->
  <xsl:apply-templates select="JOBFile/Reductions" />

</xsl:template>


<!-- **************************************************************** -->
<!-- ***************** Reductions Node Processing ******************* -->
<!-- **************************************************************** -->
<xsl:template match="Reductions">
  <xsl:apply-templates select="Point"/> 
</xsl:template>


<!-- **************************************************************** -->
<!-- **************** Grid Point Details Output ********************* -->
<!-- **************************************************************** -->
<xsl:template name="GridPoint">
  <xsl:variable name="NthStr" select="format-number(Grid/North * $DistConvFactor, $DecPl3, 'Standard')"/>

  <xsl:variable name="EastStr" select="format-number(Grid/East * $DistConvFactor, $DecPl3, 'Standard')"/>

  <xsl:variable name="ElevStr" select="format-number(Grid/Elevation * $DistConvFactor, $DecPl3, 'Standard')"/>

  <xsl:choose>
    <xsl:when test="$NECoords='true'">
      <xsl:value-of select="concat(Name, ',', $NthStr, ',', $EastStr, ',', $ElevStr, ',', Code)"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="concat(Name, ',', $EastStr, ',', $NthStr, ',', $ElevStr, ',', Code)"/>
    </xsl:otherwise>
  </xsl:choose>

</xsl:template>


<!-- **************************************************************** -->
<!-- ****************** Reductions Point Output ********************* -->
<!-- **************************************************************** -->
<xsl:template match="Point">
  
  <xsl:call-template name="GridPoint"/> 

  <!-- Now output any Feature and Attribute details associated with this point -->

  <xsl:if test="($includeAttributes = 'Yes') and Features"> <!-- Point has Features and Attributes and we are to include them -->
    <xsl:apply-templates select="Features"/>
  </xsl:if>

  <!-- Output any descriptions assigned to this point -->
  <xsl:if test="$nbrPtDescriptions &gt; 0">  <!-- There are some descriptions assigned to points -->
    <xsl:value-of select="concat(',', Description1, ',', Description2)"/>
  </xsl:if>

  <!-- Now add any note record data that may have been associated with the point in the -->
  <!-- FieldBook section or follow the point in the FieldBook section.                  -->
  <xsl:variable name="ptRecID" select="ID"/>
  <xsl:variable name="ptName" select="Name"/>
  <xsl:for-each select="/JOBFile/FieldBook/PointRecord[@ID = $ptRecID]"> <!-- Get the referenced FieldBook section PointRecord -->
	<!-- Output timestamp for this PointRecord -->
	<xsl:if test="($includeTimeStamps = 'Yes')">
		<xsl:value-of select="concat(',', @TimeStamp)"/>
	</xsl:if>
    <!-- Output any note attached to this PointRecord -->
	<xsl:if test="($includeNotes = 'Yes')">
		<xsl:for-each select="Notes">
			<xsl:value-of select="concat(',', Note)"/>
		</xsl:for-each>

		<!-- Find and output all the sequential notes that follow this point -->
		<!-- (name(.) = 'NoteRecord' - checks that the element name of the current (.) record is 'NoteRecord (it is a note) -->
		<!-- (position() = 1) - we consider the first following note as a special case (it cannot have a preceding note)    -->
		<!-- (name(preceding-sibling::*[1]) = 'NoteRecord')) - the name of the immediately preceding element is 'NoteRecord' (we have sequential notes) -->
		<!-- (preceding-sibling::PointRecord[1]/Name = $ptName) - the point record before this NoteRecord is the point we are currently working with (we haven't moved past another point) -->
		<xsl:if test="name(following-sibling::*[1]) = 'NoteRecord'">
			<xsl:for-each select="following-sibling::*[(name(.) = 'NoteRecord') and
													((position() = 1) or
													(name(preceding-sibling::*[1]) = 'NoteRecord')) and
													(preceding-sibling::PointRecord[1]/Name = $ptName)]">
				<xsl:for-each select="Notes">
					<xsl:value-of select="concat(',', Note)"/>
				</xsl:for-each>
			</xsl:for-each>
		</xsl:if>
	</xsl:if>
  </xsl:for-each>
  
  <xsl:call-template name="NewLine"/> <!-- New line ready for next point -->

</xsl:template>


<!-- **************************************************************** -->
<!-- ************** Features and Attributes Output ****************** -->
<!-- **************************************************************** -->
<xsl:template match="Features">

  <xsl:for-each select="Feature">
    <!-- Output the feature name (there may be more than 1 feature associated -->
    <!-- with the point) so this will identify which feature the attrinbutes  -->
    <!-- are associated with.                                                 -->
    <xsl:value-of select="','"/>  <!-- Comma to separate feature name from code or previous feature -->
    <xsl:variable name="FeatName" select="@Name"/> <!-- Feature name -->
    <xsl:for-each select="Attribute">
      <xsl:if test="position() &gt; 1">
        <xsl:value-of select="string(',')"/> <!-- Include a comma if not first attribute -->
      </xsl:if>
      <!-- Prefix each attribute name with the feature it belongs to followed by a ':' -->
      <xsl:value-of select="concat($FeatName, ':')"/>
      <xsl:value-of select="Name"/>
      <xsl:value-of select="string(',')"/>
      <xsl:value-of select="Value"/>
    </xsl:for-each>
  </xsl:for-each>

</xsl:template>


<!-- **************************************************************** -->
<!-- ********************** New Line Output ************************* -->
<!-- **************************************************************** -->
<xsl:template name="NewLine">
<xsl:text>&#10;</xsl:text>
</xsl:template>


</xsl:stylesheet>