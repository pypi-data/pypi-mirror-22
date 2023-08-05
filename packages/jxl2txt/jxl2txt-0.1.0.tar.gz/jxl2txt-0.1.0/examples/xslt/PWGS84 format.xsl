<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"    
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" >

<!-- (c) 2012, Trimble Navigation Limited. All rights reserved.                                -->
<!-- Permission is hereby granted to use, copy, modify, or distribute this style sheet for any -->
<!-- purpose and without fee, provided that the above copyright notice appears in all copies   -->
<!-- and that both the copyright notice and the limited warranty and restricted rights notice  -->
<!-- below appear in all supporting documentation.                                             -->

<!-- TRIMBLE NAVIGATION LIMITED PROVIDES THIS STYLE SHEET "AS IS" AND WITH ALL FAULTS.         -->
<!-- TRIMBLE NAVIGATION LIMITED SPECIFICALLY DISCLAIMS ANY IMPLIED WARRANTY OF MERCHANTABILITY -->
<!-- OR FITNESS FOR A PARTICULAR USE. TRIMBLE NAVIGATION LIMITED DOES NOT WARRANT THAT THE     -->
<!-- OPERATION OF THIS STYLE SHEET WILL BE UNINTERRUPTED OR ERROR FREE.                        -->

<xsl:output method="text" omit-xml-declaration="yes" encoding="utf-8"/>

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
                    NaN="            "
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
<xsl:variable name="DecPl6" select="concat('#0', $DecPt, '000000')"/>
<xsl:variable name="DecPl7" select="concat('#0', $DecPt, '0000000')"/>
<xsl:variable name="DecPl8" select="concat('#0', $DecPt, '00000000')"/>

<xsl:variable name="fileExt" select="'asc'"/>

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

<xsl:variable name="userField1" select="'CoordType|Coordinate Type?|stringMenu|3|ECEF|Degree-Minute-Second|Decimal Degrees'"/>
<xsl:variable name="CoordType" select="'ECEF'"/>
<!--<xsl:variable name="userField2" select="'codeSep|Kode seperator anvendt|String'"/>-->
<xsl:variable name="codeSep" select="'.'"/>
<!--<xsl:variable name="userField3" select="'AntennaHeights|Output Antenna Heights?|stringMenu|2|Yes|No'"/>-->
<xsl:variable name="AntennaHeights" select="'No'"/>

<!-- Define search keys to speed up searchs -->
<xsl:key name="PointRecordID-search" match="/JOBFile/FieldBook/PointRecord" use="@ID"/>
<xsl:key name="AntennaRecordID-search" match="/JOBFile/FieldBook/AntennaRecord" use="@ID"/>
<xsl:key name="GPSEquipmentRecordID-search" match="/JOBFile/FieldBook/GPSEquipmentRecord" use="@ID"/>

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

<xsl:variable name="Pi" select="3.14159265358979323846264"/>
<xsl:variable name="halfPi" select="$Pi div 2.0"/>
<xsl:variable name="WGS84SemiMajorAxis" select="6378137.000"/>
<xsl:variable name="WGS84Flattening" select="298.257222101"/>
<xsl:variable name="WGS84EccentricitySquared" select="0.00669438002290"/>

<!-- **************************************************************** -->
<!-- ************************** Main Loop *************************** -->
<!-- **************************************************************** -->
<xsl:template match="/" >
  <xsl:value-of select="'WG84-COORD-FILE  ,V1.00,'"/>
  <xsl:value-of select="substring-before(JOBFile/@TimeStamp, 'T')"/>  
  <xsl:call-template name="NewLine"/>  
  <xsl:choose>
    <xsl:when test="$CoordType = 'ECEF'">
	  <xsl:value-of select="'Earth Centered Earth Fixed Coordinates'"/>
	  <xsl:call-template name="NewLine"/> 
      <xsl:value-of select="'Point              X(ECEF)       Y(ECEF)       Z(ECEF)'"/>
	</xsl:when>
	<xsl:when test="$CoordType = 'Degree-Minute-Second'">
	  <xsl:value-of select="'Geographical Coordinates (Degree-Minute-Second)'"/>
	  <xsl:call-template name="NewLine"/> 
	  <xsl:value-of select="'Point                  Latitude        Longitude   Height'"/>
	</xsl:when>
	<xsl:otherwise>
	  <xsl:value-of select="'Geographical Coordinates (Decimal Degrees)'"/>
	  <xsl:call-template name="NewLine"/> 
	  <xsl:value-of select="'Point             Latitude     Longitude     Height'"/>
	</xsl:otherwise>
  </xsl:choose>
 <xsl:call-template name="NewLine"/>
 <xsl:call-template name="NewLine"/>

  <!-- Process the Point elements in the Reductions node -->
  <xsl:apply-templates select="JOBFile/Reductions/Point"/>

</xsl:template>


<!-- **************************************************************** -->
<!-- **************** Grid Point Details Output ********************* -->
<!-- **************************************************************** -->
<xsl:template match="Point">

  <xsl:if test="WGS84">
    <xsl:variable name="NameStr">
      <xsl:call-template name="PadRight">
        <xsl:with-param name="stringWidth" select="14"/>
        <xsl:with-param name="theString">
          <xsl:value-of select="Name" />
        </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="X">
      <xsl:call-template name="ecefX">
        <xsl:with-param name="latitude" select="WGS84/Latitude"/>
        <xsl:with-param name="longitude" select="WGS84/Longitude"/>
        <xsl:with-param name="height" select="WGS84/Height"/>
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="Y">
      <xsl:call-template name="ecefY">
        <xsl:with-param name="latitude" select="WGS84/Latitude"/>
        <xsl:with-param name="longitude" select="WGS84/Longitude"/>
        <xsl:with-param name="height" select="WGS84/Height"/>
      </xsl:call-template>
    </xsl:variable>
    <xsl:variable name="Z">
      <xsl:call-template name="ecefZ">
        <xsl:with-param name="latitude" select="WGS84/Latitude"/>
        <xsl:with-param name="height" select="WGS84/Height"/>
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="XStr">
      <xsl:call-template name="PadLeft">
        <xsl:with-param name="stringWidth" select="14"/>
        <xsl:with-param name="theString">
          <xsl:value-of select="format-number($X * $DistConvFactor, $DecPl3, 'Standard')" />
        </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="YStr">
      <xsl:call-template name="PadLeft">
        <xsl:with-param name="stringWidth" select="14"/>
        <xsl:with-param name="theString">
          <xsl:value-of select="format-number($Y * $DistConvFactor, $DecPl3, 'Standard')" />
        </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="ZStr">
      <xsl:call-template name="PadLeft">
        <xsl:with-param name="stringWidth" select="14"/>
        <xsl:with-param name="theString">
          <xsl:value-of select="format-number($Z * $DistConvFactor, $DecPl3, 'Standard')"/>
        </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="stdCode">
      <xsl:call-template name="PadRight">
        <xsl:with-param name="stringWidth" select="20"/>
        <xsl:with-param name="theString">
          <xsl:choose>
            <xsl:when test="contains(Code, $codeSep)">
              <xsl:value-of select="substring-before(Code, $codeSep)"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="Code"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="lineCode">
      <xsl:call-template name="PadRight">
        <xsl:with-param name="stringWidth" select="2"/>
        <xsl:with-param name="theString">
          <xsl:choose>
            <xsl:when test="contains(Code, $codeSep)">
            <xsl:value-of select="substring-after(Code, $codeSep)"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="''"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="LatStr">
      <xsl:call-template name="PadLeft">
        <xsl:with-param name="stringWidth" select="17"/>
        <xsl:with-param name="theString">
          <xsl:call-template name="FormatAngle">
            <xsl:with-param name="theAngle" select="WGS84/Latitude"/>
            <xsl:with-param name="secDecPlaces">5</xsl:with-param>
            <xsl:with-param name="DMSOutput">true</xsl:with-param>
          </xsl:call-template>
        </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="LonStr">
      <xsl:call-template name="PadLeft">
        <xsl:with-param name="stringWidth" select="17"/>
        <xsl:with-param name="theString">
          <xsl:call-template name="FormatAngle">
            <xsl:with-param name="theAngle" select="WGS84/Longitude"/>
            <xsl:with-param name="secDecPlaces">5</xsl:with-param>
            <xsl:with-param name="DMSOutput">true</xsl:with-param>
          </xsl:call-template>
        </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="HeightStr">
      <xsl:call-template name="PadLeft">
        <xsl:with-param name="stringWidth" select="9"/>
        <xsl:with-param name="theString">
          <xsl:value-of select="format-number(WGS84/Height * $DistConvFactor, $DecPl3, 'Standard')"/>
        </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="LatDecStr">
      <xsl:call-template name="PadLeft">
        <xsl:with-param name="stringWidth" select="14"/>
        <xsl:with-param name="theString">
          <xsl:value-of select="format-number(WGS84/Latitude, $DecPl8, 'Standard')" />
        </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="LonDecStr">
      <xsl:call-template name="PadLeft">
        <xsl:with-param name="stringWidth" select="14"/>
        <xsl:with-param name="theString">
          <xsl:value-of select="format-number(WGS84/Longitude, $DecPl8, 'Standard')" />
        </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="AntennaRecordID">
      <xsl:for-each select="key('PointRecordID-search', ID)">
  	  <xsl:value-of select="AntennaID"/>
  	</xsl:for-each>
    </xsl:variable>

    <xsl:variable name="MeasuredAntennaHeight">
      <xsl:call-template name="PadLeft">
        <xsl:with-param name="stringWidth" select="15"/>
        <xsl:with-param name="theString">
          <xsl:for-each select="key('AntennaRecordID-search', $AntennaRecordID)">
  	      <xsl:value-of select="format-number(MeasuredHeight * $DistConvFactor, $DecPl3, 'Standard')"/>
  	    </xsl:for-each>
  	  </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="ReducedAntennaHeight">
      <xsl:call-template name="PadLeft">
        <xsl:with-param name="stringWidth" select="13"/>
        <xsl:with-param name="theString">
          <xsl:for-each select="key('AntennaRecordID-search', $AntennaRecordID)">
  	      <xsl:value-of select="format-number(ReducedHeight * $DistConvFactor, $DecPl3, 'Standard')"/>
  	    </xsl:for-each>
  	  </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:variable name="GPSEquipmentRecordID">
      <xsl:for-each select="key('AntennaRecordID-search', $AntennaRecordID)">
  	  <xsl:value-of select="GPSEquipmentID"/>
  	</xsl:for-each>
    </xsl:variable>

    <xsl:variable name="AntMeasurementMethod">
      <xsl:call-template name="PadLeft">
        <xsl:with-param name="stringWidth" select="28"/>
        <xsl:with-param name="theString">
          <xsl:for-each select="key('GPSEquipmentRecordID-search', $GPSEquipmentRecordID)">
  	      <xsl:value-of select="AntennaMeasurementMethod"/>
  	    </xsl:for-each>
  	  </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:choose>
      <xsl:when test="$CoordType = 'ECEF'">
        <xsl:value-of select="concat($NameStr, $XStr, $YStr, $ZStr)"/>
  	</xsl:when>
  	<xsl:when test="$CoordType = 'Degree-Minute-Second'">
  	  <xsl:value-of select="concat($NameStr, $LatStr, $LonStr, $HeightStr)"/>
  	</xsl:when>
  	<xsl:otherwise>
  	  <xsl:value-of select="concat($NameStr, $LatDecStr, $LonDecStr, $HeightStr)"/>
  	</xsl:otherwise>
    </xsl:choose>

    <xsl:if test="$AntennaHeights = 'Yes'">
       <xsl:call-template name="NewLine"/>
  	 <xsl:call-template name="NewLine"/>
       <xsl:value-of select="'Meas. Ant. Hgt.                 Meas. Meth. Red. At.Hgt.'"/>
  	 <xsl:call-template name="NewLine"/>
  	 <xsl:value-of select="concat($MeasuredAntennaHeight, $AntMeasurementMethod, $ReducedAntennaHeight)"/>
  	 <xsl:call-template name="NewLine"/>
  	 <xsl:call-template name="NewLine"/>
    </xsl:if>

    <xsl:value-of select="concat(' ', $stdCode, ' ', $lineCode)"/>

    <xsl:variable name="ptNote">
      <xsl:call-template name="PadRight">
        <xsl:with-param name="stringWidth" select="12"/>
        <xsl:with-param name="theString">
          <xsl:for-each select="key('PointRecordID-search', ID)">
            <xsl:if test="name(following-sibling::*[1]) = 'NoteRecord'">
              <xsl:value-of select="following-sibling::*[1]/Notes/Note"/>
            </xsl:if>
          </xsl:for-each>
        </xsl:with-param>
      </xsl:call-template>
    </xsl:variable>

    <xsl:value-of select="$ptNote"/>
    <xsl:call-template name="NewLine"/>
  </xsl:if>
</xsl:template>


<!-- **************************************************************** -->
<!-- ****************** Return the ECEF X value ********************* -->
<!-- **************************************************************** -->
<xsl:template name="ecefX">
  <xsl:param name="latitude"/>   <!-- latitude value required in decimal degrees -->
  <xsl:param name="longitude"/>  <!-- longitude value required in decimal degrees -->
  <xsl:param name="height"/>

  <!-- Get the latitude in radians -->
  <xsl:variable name="radLat">
    <xsl:call-template name="AngleInRadians">
      <xsl:with-param name="theAngle" select="$latitude"/>
    </xsl:call-template>
  </xsl:variable>

  <!-- Get the longitude in radians -->
  <xsl:variable name="radLong">
    <xsl:call-template name="AngleInRadians">
      <xsl:with-param name="theAngle" select="$longitude"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="N">
    <xsl:call-template name="RadiusOfCurvature">
      <xsl:with-param name="latitude" select="$radLat"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="cosLat">
    <!-- Cosine of latitude = sin(Pi / 2 - latitude) -->
    <xsl:call-template name="Sine">
      <xsl:with-param name="theAngle" select="$Pi div 2.0 - $radLat"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="cosLong">
    <!-- Cosine of longitude = sin(Pi / 2 - longitude) -->
    <xsl:call-template name="Sine">
      <xsl:with-param name="theAngle" select="$Pi div 2.0 - $radLong"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:value-of select="($N + $height) * $cosLat * $cosLong"/>
</xsl:template>


<!-- **************************************************************** -->
<!-- ****************** Return the ECEF Y value ********************* -->
<!-- **************************************************************** -->
<xsl:template name="ecefY">
  <xsl:param name="latitude"/>   <!-- latitude value required in decimal degrees -->
  <xsl:param name="longitude"/>  <!-- longitude value required in decimal degrees -->
  <xsl:param name="height"/>

  <!-- Get the latitude in radians -->
  <xsl:variable name="radLat">
    <xsl:call-template name="AngleInRadians">
      <xsl:with-param name="theAngle" select="$latitude"/>
    </xsl:call-template>
  </xsl:variable>

  <!-- Get the longitude in radians -->
  <xsl:variable name="radLong">
    <xsl:call-template name="AngleInRadians">
      <xsl:with-param name="theAngle" select="$longitude"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="N">
    <xsl:call-template name="RadiusOfCurvature">
      <xsl:with-param name="latitude" select="$radLat"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="cosLat">
    <!-- Cosine of latitude = sin(Pi / 2 - latitude) -->
    <xsl:call-template name="Sine">
      <xsl:with-param name="theAngle" select="$Pi div 2.0 - $radLat"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="sinLong">
    <xsl:call-template name="Sine">
      <xsl:with-param name="theAngle" select="$radLong"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:value-of select="($N + $height) * $cosLat * $sinLong"/>
</xsl:template>


<!-- **************************************************************** -->
<!-- ****************** Return the ECEF Z value ********************* -->
<!-- **************************************************************** -->
<xsl:template name="ecefZ">
  <xsl:param name="latitude"/>  <!-- latitude value required in decimal degrees -->  
  <xsl:param name="height"/>

  <!-- Get the latitude in radians -->
  <xsl:variable name="radLat">
    <xsl:call-template name="AngleInRadians">
      <xsl:with-param name="theAngle" select="$latitude"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="N">
    <xsl:call-template name="RadiusOfCurvature">
      <xsl:with-param name="latitude" select="$radLat"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="sinLat">
    <xsl:call-template name="Sine">
      <xsl:with-param name="theAngle" select="$radLat"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:value-of select="($N * (1.0 - $WGS84EccentricitySquared) + $height) * $sinLat"/>
</xsl:template>


<!-- **************************************************************** -->
<!-- ************ Output Angle in Appropriate Format **************** -->
<!-- **************************************************************** -->
<xsl:template name="FormatAngle">
  <xsl:param name="theAngle"/>
  <xsl:param name="secDecPlaces" select="0"/>
  <xsl:param name="DMSOutput" select="'false'"/>  <!-- Can be used to force DMS output -->
  <xsl:param name="useSymbols" select="'true'"/>
  <xsl:param name="impliedDecimalPt" select="'false'"/>
  <xsl:param name="gonsDecPlaces" select="5"/>    <!-- Decimal places for gons output -->
  <xsl:param name="decDegDecPlaces" select="5"/>  <!-- Decimal places for decimal degrees output -->
  <xsl:param name="outputAsMilligonsOrSecs" select="'false'"/>
  <xsl:param name="outputAsMilligonsOrSecsSqrd" select="'false'"/>
  <xsl:param name="dmsSymbols">&#0176;'"</xsl:param>

  <xsl:variable name="gonsDecPl">
    <xsl:choose>
      <xsl:when test="$gonsDecPlaces = 1"><xsl:value-of select="$DecPl1"/></xsl:when>
      <xsl:when test="$gonsDecPlaces = 2"><xsl:value-of select="$DecPl2"/></xsl:when>
      <xsl:when test="$gonsDecPlaces = 3"><xsl:value-of select="$DecPl3"/></xsl:when>
      <xsl:when test="$gonsDecPlaces = 4"><xsl:value-of select="$DecPl4"/></xsl:when>
      <xsl:when test="$gonsDecPlaces = 5"><xsl:value-of select="$DecPl5"/></xsl:when>
      <xsl:when test="$gonsDecPlaces = 6"><xsl:value-of select="$DecPl6"/></xsl:when>
    </xsl:choose>
  </xsl:variable>

  <xsl:variable name="decDegDecPl">
    <xsl:choose>
      <xsl:when test="$decDegDecPlaces = 1"><xsl:value-of select="$DecPl1"/></xsl:when>
      <xsl:when test="$decDegDecPlaces = 2"><xsl:value-of select="$DecPl2"/></xsl:when>
      <xsl:when test="$decDegDecPlaces = 3"><xsl:value-of select="$DecPl3"/></xsl:when>
      <xsl:when test="$decDegDecPlaces = 4"><xsl:value-of select="$DecPl4"/></xsl:when>
      <xsl:when test="$decDegDecPlaces = 5"><xsl:value-of select="$DecPl5"/></xsl:when>
      <xsl:when test="$decDegDecPlaces = 6"><xsl:value-of select="$DecPl6"/></xsl:when>
    </xsl:choose>
  </xsl:variable>

  <xsl:choose>
    <!-- Null angle value -->
    <xsl:when test="string(number($theAngle))='NaN'">
      <xsl:value-of select="format-number($theAngle, $DecPl3, 'Standard')"/> <!-- Use the defined null format output -->
    </xsl:when>
    <!-- There is an angle value -->
    <xsl:otherwise>
      <xsl:choose>
        <xsl:when test="($AngleUnit = 'DMSDegrees') or not($DMSOutput = 'false')">
          <xsl:choose>
            <xsl:when test="$outputAsMilligonsOrSecs != 'false'">
              <xsl:value-of select="format-number($theAngle * $AngleConvFactor * 3600.0, '00.0', 'Standard')"/>
            </xsl:when>            
            <xsl:when test="$outputAsMilligonsOrSecsSqrd != 'false'">
              <xsl:value-of select="format-number($theAngle * $AngleConvFactor * 3600.0 * 3600.0, '00.000', 'Standard')"/>
            </xsl:when>            
            <xsl:otherwise>
              <xsl:call-template name="FormatDMSAngle">
                <xsl:with-param name="decimalAngle" select="$theAngle"/>
                <xsl:with-param name="secDecPlaces" select="$secDecPlaces"/>
                <xsl:with-param name="useSymbols" select="$useSymbols"/>
                <xsl:with-param name="impliedDecimalPt" select="$impliedDecimalPt"/>
                <xsl:with-param name="dmsSymbols" select="$dmsSymbols"/>
              </xsl:call-template>
            </xsl:otherwise>
          </xsl:choose>  
        </xsl:when>

        <xsl:otherwise>
          <xsl:variable name="fmtAngle">
            <xsl:choose>
              <xsl:when test="($AngleUnit = 'Gons') and ($DMSOutput = 'false')">
                <xsl:choose>
                  <xsl:when test="$outputAsMilligonsOrSecs != 'false'">
                    <xsl:value-of select="format-number($theAngle * $AngleConvFactor * 1000.0, $DecPl2, 'Standard')"/>
                  </xsl:when>
                  <xsl:when test="$outputAsMilligonsOrSecsSqrd != 'false'">
                    <xsl:value-of select="format-number($theAngle * $AngleConvFactor * 1000.0 * 1000.0, $DecPl4, 'Standard')"/>
                  </xsl:when>
                  <xsl:otherwise>
                    <xsl:choose>
                      <xsl:when test="$secDecPlaces &gt; 0">  <!-- More accurate angle output required -->
                        <xsl:value-of select="format-number($theAngle * $AngleConvFactor, $DecPl8, 'Standard')"/>
                      </xsl:when>
                      <xsl:otherwise>
                        <xsl:value-of select="format-number($theAngle * $AngleConvFactor, $gonsDecPl, 'Standard')"/>
                      </xsl:otherwise>
                    </xsl:choose>
                  </xsl:otherwise>
                </xsl:choose>
              </xsl:when>

              <xsl:when test="($AngleUnit = 'Mils') and ($DMSOutput = 'false')">
                <xsl:choose>
                  <xsl:when test="$secDecPlaces &gt; 0">  <!-- More accurate angle output required -->
                    <xsl:value-of select="format-number($theAngle * $AngleConvFactor, $DecPl6, 'Standard')"/>
                  </xsl:when>
                  <xsl:otherwise>
                    <xsl:value-of select="format-number($theAngle * $AngleConvFactor, $DecPl4, 'Standard')"/>
                  </xsl:otherwise>
                </xsl:choose>
              </xsl:when>

              <xsl:when test="($AngleUnit = 'DecimalDegrees') and ($DMSOutput = 'false')">
                <xsl:choose>
                  <xsl:when test="$secDecPlaces &gt; 0">  <!-- More accurate angle output required -->
                    <xsl:value-of select="format-number($theAngle * $AngleConvFactor, $DecPl8, 'Standard')"/>
                  </xsl:when>
                  <xsl:otherwise>
                    <xsl:value-of select="format-number($theAngle * $AngleConvFactor, $decDegDecPl, 'Standard')"/>
                  </xsl:otherwise>
                </xsl:choose>
              </xsl:when>
            </xsl:choose>
          </xsl:variable>
          
          <xsl:choose>
            <xsl:when test="$impliedDecimalPt != 'true'">
              <xsl:value-of select="$fmtAngle"/>
            </xsl:when>
            <xsl:otherwise>
              <xsl:value-of select="translate($fmtAngle, '.', '')"/>
            </xsl:otherwise>
          </xsl:choose>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>


<!-- **************************************************************** -->
<!-- *********** Pad a string to the right with spaces ************** -->
<!-- **************************************************************** -->
<xsl:template name="PadRight">
  <xsl:param name="stringWidth"/>
  <xsl:param name="theString"/>
  <xsl:choose>
    <xsl:when test="$stringWidth = '0'">
      <xsl:value-of select="normalize-space($theString)"/> <!-- Function return value -->
    </xsl:when>
    <xsl:otherwise>
      <xsl:variable name="paddedStr" select="concat($theString, '                                                                                          ')"/>
      <xsl:value-of select="substring($paddedStr, 1, $stringWidth)"/> <!-- Function return value -->
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>


<!-- **************************************************************** -->
<!-- *********** Pad a string to the left with spaces *************** -->
<!-- **************************************************************** -->
<xsl:template name="PadLeft">
  <xsl:param name="stringWidth"/>
  <xsl:param name="theString"/>
  <xsl:choose>
    <xsl:when test="$stringWidth = '0'">
      <xsl:value-of select="normalize-space($theString)"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:variable name="paddedStr" select="concat('                                                            ', $theString)"/>
      <xsl:value-of select="substring($paddedStr, string-length($paddedStr) - $stringWidth + 1)"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>


<!-- **************************************************************** -->
<!-- ********************** New Line Output ************************* -->
<!-- **************************************************************** -->
<xsl:template name="NewLine">
  <xsl:text>&#10;</xsl:text>
</xsl:template>


<!-- **************************************************************** -->
<!-- ********************** Angle in Radians ************************ -->
<!-- **************************************************************** -->
<xsl:template name="AngleInRadians">
  <xsl:param name="theAngle"/>
  <xsl:param name="normalise" select="'false'"/>
  <xsl:choose>
    <!-- Null angle value -->
    <xsl:when test="string(number($theAngle)) = 'NaN'">
      <xsl:value-of select="''"/>
    </xsl:when>
    <!-- There is an angle value -->
    <xsl:otherwise>
      <xsl:variable name="radiansAngle">
        <xsl:value-of select="$theAngle * $Pi div 180.0"/>
      </xsl:variable>

      <xsl:variable name="outAngle">
        <xsl:choose>
          <xsl:when test="$normalise = 'false'">
            <xsl:value-of select="$radiansAngle"/>
          </xsl:when>
          <xsl:otherwise>
            <xsl:call-template name="RadianAngleBetweenLimits">
              <xsl:with-param name="anAngle" select="$radiansAngle"/>
            </xsl:call-template>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:variable>
      <xsl:value-of select="$outAngle"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>


<!-- **************************************************************** -->
<!-- ************ Return the sine of an angle in radians ************ -->
<!-- **************************************************************** -->
<xsl:template name="Sine">
  <xsl:param name="theAngle"/>
  <xsl:variable name="normalisedAngle">
    <xsl:call-template name="RadianAngleBetweenLimits">
      <xsl:with-param name="anAngle" select="$theAngle"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="theSine">
    <xsl:call-template name="sineIter">
      <xsl:with-param name="pX2" select="$normalisedAngle * $normalisedAngle"/>
      <xsl:with-param name="pRslt" select="$normalisedAngle"/>
      <xsl:with-param name="pElem" select="$normalisedAngle"/>
      <xsl:with-param name="pN" select="1"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:value-of select="number($theSine)"/>
</xsl:template>

<xsl:template name="sineIter">
  <xsl:param name="pX2"/>
  <xsl:param name="pRslt"/>
  <xsl:param name="pElem"/>
  <xsl:param name="pN"/>
  <xsl:param name="pEps" select="0.00000001"/>
  <xsl:variable name="vnextN" select="$pN+2"/>
  <xsl:variable name="vnewElem"  select="-$pElem*$pX2 div ($vnextN*($vnextN - 1))"/>
  <xsl:variable name="vnewResult" select="$pRslt + $vnewElem"/>
  <xsl:variable name="vdiffResult" select="$vnewResult - $pRslt"/>
  <xsl:choose>
    <xsl:when test="$vdiffResult > $pEps or $vdiffResult &lt; -$pEps">
      <xsl:call-template name="sineIter">
        <xsl:with-param name="pX2" select="$pX2"/>
        <xsl:with-param name="pRslt" select="$vnewResult"/>
        <xsl:with-param name="pElem" select="$vnewElem"/>
        <xsl:with-param name="pN" select="$vnextN"/>
        <xsl:with-param name="pEps" select="$pEps"/>
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$vnewResult"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>


<!-- **************************************************************** -->
<!-- ******* Return the Radius of Curvature in Prime Vertical ******* -->
<!-- **************************************************************** -->
<xsl:template name="RadiusOfCurvature">
  <xsl:param name="latitude"/>   <!-- Already converted to radians -->

  <xsl:variable name="sinLat">
    <xsl:call-template name="Sine">
      <xsl:with-param name="theAngle" select="$latitude"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="sinLatSquared">
    <xsl:value-of select="$sinLat * $sinLat"/>
  </xsl:variable>

  <xsl:variable name="tempVal">
    <xsl:call-template name="Sqrt">
      <xsl:with-param name="num" select="1.0 - $WGS84EccentricitySquared * $sinLatSquared"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:value-of select="$WGS84SemiMajorAxis div $tempVal"/>
</xsl:template>


<!-- **************************************************************** -->
<!-- ********************** Format a DMS Angle ********************** -->
<!-- **************************************************************** -->
<xsl:template name="FormatDMSAngle">
  <xsl:param name="decimalAngle"/>
  <xsl:param name="secDecPlaces" select="0"/>
  <xsl:param name="useSymbols" select="'true'"/>
  <xsl:param name="impliedDecimalPt" select="'false'"/>
  <xsl:param name="dmsSymbols">&#0176;'"</xsl:param>

  <xsl:variable name="degreesSymbol">
    <xsl:choose>
      <xsl:when test="$useSymbols = 'true'"><xsl:value-of select="substring($dmsSymbols, 1, 1)"/></xsl:when>  <!-- Degrees symbol ° -->
      <xsl:otherwise>
        <xsl:if test="$impliedDecimalPt != 'true'">.</xsl:if>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <xsl:variable name="minutesSymbol">
    <xsl:choose>
      <xsl:when test="$useSymbols = 'true'"><xsl:value-of select="substring($dmsSymbols, 2, 1)"/></xsl:when>
      <xsl:otherwise></xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <xsl:variable name="secondsSymbol">
    <xsl:choose>
      <xsl:when test="$useSymbols = 'true'"><xsl:value-of select="substring($dmsSymbols, 3, 1)"/></xsl:when>
      <xsl:otherwise></xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <xsl:variable name="sign">
    <xsl:if test="$decimalAngle &lt; '0.0'">-1</xsl:if>
    <xsl:if test="$decimalAngle &gt;= '0.0'">1</xsl:if>
  </xsl:variable>

  <xsl:variable name="posDecimalDegrees" select="number($decimalAngle * $sign)"/>

  <xsl:variable name="positiveDecimalDegrees">  <!-- Ensure an angle very close to 360° is treated as 0° -->
    <xsl:choose>
      <xsl:when test="(360.0 - $posDecimalDegrees) &lt; 0.00001">
        <xsl:value-of select="0"/>
      </xsl:when>
      <xsl:otherwise>
        <xsl:value-of select="$posDecimalDegrees"/>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <xsl:variable name="decPlFmt">
    <xsl:choose>
      <xsl:when test="$secDecPlaces = 0"><xsl:value-of select="''"/></xsl:when>
      <xsl:when test="$secDecPlaces = 1"><xsl:value-of select="'.0'"/></xsl:when>
      <xsl:when test="$secDecPlaces = 2"><xsl:value-of select="'.00'"/></xsl:when>
      <xsl:when test="$secDecPlaces = 3"><xsl:value-of select="'.000'"/></xsl:when>
      <xsl:when test="$secDecPlaces = 4"><xsl:value-of select="'.0000'"/></xsl:when>
      <xsl:when test="$secDecPlaces = 5"><xsl:value-of select="'.00000'"/></xsl:when>
      <xsl:when test="$secDecPlaces = 6"><xsl:value-of select="'.000000'"/></xsl:when>
      <xsl:otherwise><xsl:value-of select="''"/></xsl:otherwise>
    </xsl:choose>
  </xsl:variable>

  <xsl:variable name="degrees" select="floor($positiveDecimalDegrees)"/>
  <xsl:variable name="decimalMinutes" select="number(number($positiveDecimalDegrees - $degrees) * 60 )"/>
  <xsl:variable name="minutes" select="floor($decimalMinutes)"/>
  <xsl:variable name="seconds" select="number(number($decimalMinutes - $minutes)*60)"/>

  <xsl:variable name="partiallyNormalisedMinutes">
    <xsl:if test="number(format-number($seconds, concat('00', $decPlFmt))) = 60"><xsl:value-of select="number($minutes + 1)"/></xsl:if>
    <xsl:if test="not(number(format-number($seconds, concat('00', $decPlFmt))) = 60)"><xsl:value-of select="$minutes"/></xsl:if>
  </xsl:variable>

  <xsl:variable name="normalisedSeconds">
    <xsl:if test="number(format-number($seconds, concat('00', $decPlFmt))) = 60"><xsl:value-of select="0"/></xsl:if>
    <xsl:if test="not(number(format-number($seconds, concat('00', $decPlFmt))) = 60)"><xsl:value-of select="$seconds"/></xsl:if>
  </xsl:variable>

  <xsl:variable name="partiallyNormalisedDegrees">
    <xsl:if test="format-number($partiallyNormalisedMinutes, '0') = '60'"><xsl:value-of select="number($degrees + 1)"/></xsl:if>
    <xsl:if test="not(format-number($partiallyNormalisedMinutes, '0') = '60')"><xsl:value-of select="$degrees"/></xsl:if>
  </xsl:variable>

  <xsl:variable name="normalisedDegrees">
    <xsl:if test="format-number($partiallyNormalisedDegrees, '0') = '360'"><xsl:value-of select="0"/></xsl:if>
    <xsl:if test="not(format-number($partiallyNormalisedDegrees, '0') = '360')"><xsl:value-of select="$partiallyNormalisedDegrees"/></xsl:if>
  </xsl:variable>

  <xsl:variable name="normalisedMinutes">
    <xsl:if test="format-number($partiallyNormalisedMinutes, '00') = '60'"><xsl:value-of select="0"/></xsl:if>
    <xsl:if test="not(format-number($partiallyNormalisedMinutes, '00') = '60')"><xsl:value-of select="$partiallyNormalisedMinutes"/></xsl:if>
  </xsl:variable>

  <xsl:if test="$sign = -1">-</xsl:if>
  <xsl:value-of select="format-number($normalisedDegrees, '0')"/>
  <xsl:value-of select="$degreesSymbol"/>
  <xsl:value-of select="format-number($normalisedMinutes, '00')"/>
  <xsl:value-of select="$minutesSymbol"/>
  <xsl:choose>
    <xsl:when test="$useSymbols = 'true'">
      <xsl:value-of select="format-number($normalisedSeconds, concat('00', $decPlFmt))"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="translate(format-number($normalisedSeconds, concat('00', $decPlFmt)), '.', '')"/>
    </xsl:otherwise>
  </xsl:choose>
  <xsl:value-of select="$secondsSymbol"/>
</xsl:template>


<!-- **************************************************************** -->
<!-- ********* Return radians angle between Specified Limits ******** -->
<!-- **************************************************************** -->
<xsl:template name="RadianAngleBetweenLimits">
  <xsl:param name="anAngle"/>
  <xsl:param name="minVal" select="0.0"/>
  <xsl:param name="maxVal" select="$Pi * 2.0"/>
  <xsl:param name="incVal" select="$Pi * 2.0"/>

  <xsl:variable name="angle1">
    <xsl:call-template name="AngleValueLessThanMax">
      <xsl:with-param name="inAngle" select="$anAngle"/>
      <xsl:with-param name="maxVal" select="$maxVal"/>
      <xsl:with-param name="incVal" select="$incVal"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:variable name="angle2">
    <xsl:call-template name="AngleValueGreaterThanMin">
      <xsl:with-param name="inAngle" select="$angle1"/>
      <xsl:with-param name="minVal" select="$minVal"/>
      <xsl:with-param name="incVal" select="$incVal"/>
    </xsl:call-template>
  </xsl:variable>

  <xsl:value-of select="$angle2"/>
</xsl:template>


<!-- **************************************************************** -->
<!-- *************** Return the square root of a value ************** -->
<!-- **************************************************************** -->
<xsl:template name="Sqrt">
  <xsl:param name="num" select="0"/>       <!-- The number you want to find the square root of -->
  <xsl:param name="try" select="1"/>       <!-- The current 'try'.  This is used internally. -->
  <xsl:param name="iter" select="1"/>      <!-- The current iteration, checked against maxiter to limit loop count - used internally -->
  <xsl:param name="maxiter" select="40"/>  <!-- Set this up to insure against infinite loops - used internally -->

  <!-- This template uses Sir Isaac Newton's method of finding roots -->

  <xsl:choose>
    <xsl:when test="$num &lt; 0"></xsl:when>  <!-- Invalid input - no square root of a negative number so return null -->
    <xsl:when test="$try * $try = $num or $iter &gt; $maxiter">
      <xsl:value-of select="$try"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:call-template name="Sqrt">
        <xsl:with-param name="num" select="$num"/>
        <xsl:with-param name="try" select="$try - (($try * $try - $num) div (2 * $try))"/>
        <xsl:with-param name="iter" select="$iter + 1"/>
        <xsl:with-param name="maxiter" select="$maxiter"/>
      </xsl:call-template>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>


<!-- **************************************************************** -->
<!-- ******* Return radians angle less than Specificed Maximum ****** -->
<!-- **************************************************************** -->
<xsl:template name="AngleValueLessThanMax">
  <xsl:param name="inAngle"/>
  <xsl:param name="maxVal"/>
  <xsl:param name="incVal"/>

  <xsl:choose>
    <xsl:when test="$inAngle &gt; $maxVal">
      <xsl:variable name="newAngle">
        <xsl:value-of select="$inAngle - $incVal"/>
      </xsl:variable>
      <xsl:call-template name="AngleValueLessThanMax">
        <xsl:with-param name="inAngle" select="$newAngle"/>
      </xsl:call-template>
    </xsl:when>

    <xsl:otherwise>
      <xsl:value-of select="$inAngle"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>


<!-- **************************************************************** -->
<!-- ************* Return radians angle greater than Zero *********** -->
<!-- **************************************************************** -->
<xsl:template name="AngleValueGreaterThanMin">
  <xsl:param name="inAngle"/>
  <xsl:param name="minVal"/>
  <xsl:param name="incVal"/>

  <xsl:choose>
    <xsl:when test="$inAngle &lt; $minVal">
      <xsl:variable name="newAngle">
        <xsl:value-of select="$inAngle + $incVal"/>
      </xsl:variable>
      <xsl:call-template name="AngleValueGreaterThanMin">
        <xsl:with-param name="inAngle" select="$newAngle"/>
      </xsl:call-template>
    </xsl:when>

    <xsl:otherwise>
      <xsl:value-of select="$inAngle"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>


</xsl:stylesheet>
