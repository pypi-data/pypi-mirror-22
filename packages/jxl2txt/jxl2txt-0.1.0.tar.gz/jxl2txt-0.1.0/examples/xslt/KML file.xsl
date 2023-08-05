<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"    
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:kml="http://earth.google.com/kml/2.2"
    xmlns:msxsl="urn:schemas-microsoft-com:xslt">
    
<!-- (c) 2012, Trimble Navigation Limited. All rights reserved.                                -->
<!-- Permission is hereby granted to use, copy, modify, or distribute this style sheet for any -->
<!-- purpose and without fee, provided that the above copyright notice appears in all copies   -->
<!-- and that both the copyright notice and the limited warranty and restricted rights notice  -->
<!-- below appear in all supporting documentation.                                             -->

<!-- TRIMBLE NAVIGATION LIMITED PROVIDES THIS STYLE SHEET "AS IS" AND WITH ALL FAULTS.         -->
<!-- TRIMBLE NAVIGATION LIMITED SPECIFICALLY DISCLAIMS ANY IMPLIED WARRANTY OF MERCHANTABILITY -->
<!-- OR FITNESS FOR A PARTICULAR USE. TRIMBLE NAVIGATION LIMITED DOES NOT WARRANT THAT THE     -->
<!-- OPERATION OF THIS STYLE SHEET WILL BE UNINTERRUPTED OR ERROR FREE.                        -->

<xsl:output method="xml" omit-xml-declaration="no" encoding="utf-8"/>

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
                    NaN=""
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
<xsl:variable name="DecPl10" select="concat('#0', $DecPt, '0000000000')"/>

<xsl:variable name="fileExt" select="'kml'"/>

<xsl:variable name="pixelWidthForImages">500</xsl:variable>

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

<xsl:variable name="distAbbrev">
  <xsl:choose>
    <xsl:when test="$DistUnit='Metres'">m</xsl:when>
    <xsl:when test="$DistUnit='InternationalFeet'">ift</xsl:when>
    <xsl:when test="$DistUnit='USSurveyFeet'">sft</xsl:when>
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


<!-- **************************************************************** -->
<!-- ************************** Main Loop *************************** -->
<!-- **************************************************************** -->
<xsl:template match="/" >

  <xsl:call-template name="NewLine"/>
  <xsl:element name="kml" namespace="http://earth.google.com/kml/2.2">
    <xsl:call-template name="NewLine"/>
    <xsl:element name="Document" namespace="http://earth.google.com/kml/2.2">
      <xsl:call-template name="NewLine"/>
      <xsl:element name="name" namespace="http://earth.google.com/kml/2.2">
        <xsl:value-of select="JOBFile/@jobName"/>
      </xsl:element>
      <xsl:call-template name="NewLine"/>
      <xsl:call-template name="StyleDefinitions"/>
      <xsl:apply-templates select="JOBFile/Reductions/Point[WGS84]"/>
    </xsl:element>
    <xsl:call-template name="NewLine"/>
  </xsl:element>
  <xsl:call-template name="NewLine"/>

</xsl:template>


<!-- **************************************************************** -->
<!-- ***************** Reductions Node Processing ******************* -->
<!-- **************************************************************** -->
<xsl:template match="Point">

  <xsl:element name="Placemark" namespace="http://earth.google.com/kml/2.2"><xsl:call-template name="NewLine"/>

    <xsl:element name="name" namespace="http://earth.google.com/kml/2.2">
      <xsl:value-of select="Name"/>
    </xsl:element><xsl:call-template name="NewLine"/>

    <xsl:element name="description" namespace="http://earth.google.com/kml/2.2">
      <xsl:text disable-output-escaping="yes">&lt;font color="#0000ff"&gt;</xsl:text>  <!-- Set blue text -->
      <xsl:value-of select="Code"/>
      <xsl:text disable-output-escaping="yes">&lt;/font&gt;</xsl:text>
      
      <!-- Add any features and attribute details for the point -->
      <xsl:text disable-output-escaping="yes">&lt;font color="#000000"&gt;</xsl:text>  <!-- Set black text -->
      <xsl:apply-templates select="Features"/>
      <!-- Now add a break and the point's grid coordinates -->
      <xsl:text disable-output-escaping="yes">&lt;dl&gt;&lt;dt&gt;Grid:&lt;/dt&gt;</xsl:text>
      <xsl:choose>
        <xsl:when test="$NECoords = 'true'">
          <xsl:text disable-output-escaping="yes">&lt;dd&gt;</xsl:text>
          <xsl:value-of select="format-number(Grid/North * $DistConvFactor, $DecPl3, 'Standard')"/>
          <xsl:value-of select="$distAbbrev"/>
          <xsl:text disable-output-escaping="yes">N&lt;/dd&gt;&lt;dd&gt;</xsl:text>
          <xsl:value-of select="format-number(Grid/East * $DistConvFactor, $DecPl3, 'Standard')"/>
          <xsl:value-of select="$distAbbrev"/>
          <xsl:text disable-output-escaping="yes">E&lt;/dd&gt;</xsl:text>
        </xsl:when>
        <xsl:otherwise>
          <xsl:text disable-output-escaping="yes">&lt;dd&gt;</xsl:text>
          <xsl:value-of select="format-number(Grid/East * $DistConvFactor, $DecPl3, 'Standard')"/>
          <xsl:value-of select="$distAbbrev"/>
          <xsl:text disable-output-escaping="yes">E&lt;/dd&gt;&lt;dd&gt;</xsl:text>
          <xsl:value-of select="format-number(Grid/North * $DistConvFactor, $DecPl3, 'Standard')"/>
          <xsl:value-of select="$distAbbrev"/>
          <xsl:text disable-output-escaping="yes">N&lt;/dd&gt;</xsl:text>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:text disable-output-escaping="yes">&lt;dd&gt;</xsl:text>
      <xsl:value-of select="format-number(Grid/Elevation * $DistConvFactor, $DecPl3, 'Standard')"/>
      <xsl:value-of select="$distAbbrev"/>
      <xsl:text disable-output-escaping="yes">El&lt;/dd&gt;</xsl:text>
      <xsl:text disable-output-escaping="yes">&lt;/dl&gt;</xsl:text>
      <xsl:text disable-output-escaping="yes">&lt;/font&gt;</xsl:text>
      
      <!-- Include photo in pop-up box if assigned to the point -->
      <xsl:variable name="imageFileNames">
        <!-- Get any Photo attributes -->
        <xsl:for-each select="Features/Feature/Attribute[(Type = 'Photo') and (Value != '')]">
          <xsl:element name="file">
            <xsl:value-of select="translate(Value,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"/>
          </xsl:element>
        </xsl:for-each>

        <!-- Get any File attributes where the file name has a .jpg extension -->
        <xsl:for-each select="Features/Feature/Attribute[(Type = 'File') and ((contains(Value, '.jpg')) or (contains(Value, '.JPG')))]">
          <xsl:element name="file">
            <xsl:value-of select="translate(Value,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"/>
          </xsl:element>
        </xsl:for-each>

        <!-- Get any MediaFileRecord elements that reference the current point -->
        <xsl:variable name="ptRecID" select="ID"/>
        <xsl:for-each select="/JOBFile/FieldBook/MediaFileRecord[RecordID = $ptRecID]">
          <xsl:element name="file">
            <xsl:value-of select="translate(FileName,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"/>
          </xsl:element>
        </xsl:for-each>

        <!-- Get any ImageRecord elements that reference the current point -->
        <xsl:for-each select="/JOBFile/FieldBook/ImageRecord[PointRecordID = $ptRecID]">
          <xsl:element name="file">
            <xsl:value-of select="translate(FileName,'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz')"/>
          </xsl:element>
        </xsl:for-each>
      </xsl:variable>

      <xsl:if test="count(msxsl:node-set($imageFileNames)/file) != 0">
        <xsl:for-each select="msxsl:node-set($imageFileNames)/file[1]">
          <!-- Grab the first photo reference -->
          <xsl:text disable-output-escaping="yes">&lt;img src="</xsl:text>
          <xsl:value-of select="."/>
          <xsl:text>" width="</xsl:text>
          <xsl:value-of select="$pixelWidthForImages"/>
          <xsl:text disable-output-escaping="yes">"/&gt;</xsl:text>
        </xsl:for-each>
      </xsl:if>
    </xsl:element><xsl:call-template name="NewLine"/>

    <xsl:variable name="ptID" select="ID"/>
    <xsl:choose>
      <xsl:when test="/JOBFile/FieldBook/PointRecord[@ID = $ptID][Classification = 'Control']">
        <xsl:element name="styleUrl" namespace="http://earth.google.com/kml/2.2">#controlPoint</xsl:element>
      </xsl:when>
      <xsl:otherwise>
        <xsl:element name="styleUrl" namespace="http://earth.google.com/kml/2.2">#standardPoint</xsl:element>
      </xsl:otherwise>
    </xsl:choose>
    <xsl:call-template name="NewLine"/>
    
    <xsl:element name="Point" namespace="http://earth.google.com/kml/2.2"><xsl:call-template name="NewLine"/>
      <xsl:element name="coordinates" namespace="http://earth.google.com/kml/2.2">
        <xsl:value-of select="concat(WGS84/Longitude, ',', WGS84/Latitude, ',', WGS84/Height)"/>
      </xsl:element><xsl:call-template name="NewLine"/>
    </xsl:element><xsl:call-template name="NewLine"/>
  </xsl:element>
  <xsl:call-template name="NewLine"/>
</xsl:template>


<!-- **************************************************************** -->
<!-- ****************** Features Node Processing ******************** -->
<!-- **************************************************************** -->
<xsl:template match="Features">
  <xsl:text disable-output-escaping="yes">&lt;br/&gt;Attributes:</xsl:text>
  <xsl:for-each select="Feature">
    <xsl:text disable-output-escaping="yes">&lt;dl&gt;&lt;dt&gt;</xsl:text>  <!-- Start list -->
    <xsl:value-of select="@Name"/>
    <xsl:text disable-output-escaping="yes">&lt;/dt&gt;</xsl:text>

      <xsl:for-each select="Attribute">
        <xsl:text disable-output-escaping="yes">&lt;dd&gt;</xsl:text>        <!-- Start list item -->
        <xsl:value-of select="Name"/>
        <xsl:text>: </xsl:text>
        <xsl:value-of select="Value"/>
        <xsl:text disable-output-escaping="yes">&lt;/dd&gt;</xsl:text>       <!-- End list item -->
      </xsl:for-each>

    <xsl:text disable-output-escaping="yes">&lt;/dl&gt;</xsl:text>           <!-- End list -->
  </xsl:for-each>
</xsl:template>


<!-- **************************************************************** -->
<!-- ************** Output point style definitions ****************** -->
<!-- **************************************************************** -->
<xsl:template name="StyleDefinitions">
  <xsl:element name="Style" namespace="http://earth.google.com/kml/2.2">
    <xsl:attribute name="id">controlPoint</xsl:attribute>
    <xsl:call-template name="NewLine"/>
    <xsl:element name="IconStyle" namespace="http://earth.google.com/kml/2.2">
      <xsl:call-template name="NewLine"/>
      <xsl:element name="scale" namespace="http://earth.google.com/kml/2.2">0.5</xsl:element>
      <xsl:call-template name="NewLine"/>
      <xsl:element name="Icon" namespace="http://earth.google.com/kml/2.2">
        <xsl:call-template name="NewLine"/>
        <xsl:element name="href" namespace="http://earth.google.com/kml/2.2">http://maps.google.com/mapfiles/kml/pal4/icon49.png</xsl:element>
        <xsl:call-template name="NewLine"/>
      </xsl:element>
      <xsl:call-template name="NewLine"/>
    </xsl:element>
    <xsl:call-template name="NewLine"/>

    <xsl:element name="LabelStyle" namespace="http://earth.google.com/kml/2.2">
      <xsl:element name="color" namespace="http://earth.google.com/kml/2.2">ff0000ff</xsl:element>
      <xsl:call-template name="NewLine"/>
      <xsl:element name="colorMode" namespace="http://earth.google.com/kml/2.2">normal</xsl:element>
      <xsl:call-template name="NewLine"/>
      <xsl:element name="scale" namespace="http://earth.google.com/kml/2.2">0.6</xsl:element>
      <xsl:call-template name="NewLine"/>
    </xsl:element>
    <xsl:call-template name="NewLine"/>

    <xsl:element name="BalloonStyle" namespace="http://earth.google.com/kml/2.2">
      <xsl:call-template name="NewLine"/>
      <xsl:element name="text" namespace="http://earth.google.com/kml/2.2">
        <xsl:text disable-output-escaping="yes">&lt;![CDATA[</xsl:text>
        <xsl:call-template name="NewLine"/>
        <xsl:text disable-output-escaping="yes">Point: &lt;b&gt;&lt;font color="#ff0000"&gt;$[name]&lt;/font&gt;&lt;/b&gt;</xsl:text>
        <xsl:call-template name="NewLine"/>
        <xsl:text disable-output-escaping="yes">&lt;br/&gt;</xsl:text>
        <xsl:call-template name="NewLine"/>
        <xsl:text disable-output-escaping="yes">Code: $[description]</xsl:text>
        <xsl:call-template name="NewLine"/>
        <xsl:text disable-output-escaping="yes">]]&gt;</xsl:text>
      </xsl:element>
      <xsl:call-template name="NewLine"/>
    </xsl:element>
    <xsl:call-template name="NewLine"/>

  </xsl:element>
  <xsl:call-template name="NewLine"/>

  <xsl:element name="Style" namespace="http://earth.google.com/kml/2.2">
    <xsl:attribute name="id">standardPoint</xsl:attribute>
    <xsl:call-template name="NewLine"/>
    <xsl:element name="IconStyle" namespace="http://earth.google.com/kml/2.2">
      <xsl:call-template name="NewLine"/>
      <xsl:element name="scale" namespace="http://earth.google.com/kml/2.2">0.5</xsl:element>
      <xsl:call-template name="NewLine"/>
      <xsl:element name="Icon" namespace="http://earth.google.com/kml/2.2">
        <xsl:call-template name="NewLine"/>
        <xsl:element name="href" namespace="http://earth.google.com/kml/2.2">http://maps.google.com/mapfiles/kml/pal4/icon57.png</xsl:element>
        <xsl:call-template name="NewLine"/>
      </xsl:element>
      <xsl:call-template name="NewLine"/>
    </xsl:element>
    <xsl:call-template name="NewLine"/>

    <xsl:element name="LabelStyle" namespace="http://earth.google.com/kml/2.2">
      <xsl:element name="color" namespace="http://earth.google.com/kml/2.2">ff0000ff</xsl:element>
      <xsl:call-template name="NewLine"/>
      <xsl:element name="colorMode" namespace="http://earth.google.com/kml/2.2">normal</xsl:element>
      <xsl:call-template name="NewLine"/>
      <xsl:element name="scale" namespace="http://earth.google.com/kml/2.2">0.6</xsl:element>
      <xsl:call-template name="NewLine"/>
    </xsl:element>
    <xsl:call-template name="NewLine"/>

    <xsl:element name="BalloonStyle" namespace="http://earth.google.com/kml/2.2">
      <xsl:call-template name="NewLine"/>
      <xsl:element name="text" namespace="http://earth.google.com/kml/2.2">
        <xsl:text disable-output-escaping="yes">&lt;![CDATA[</xsl:text>
        <xsl:call-template name="NewLine"/>
        <xsl:text disable-output-escaping="yes">Point: &lt;b&gt;&lt;font color="#ff0000"&gt;$[name]&lt;/font&gt;&lt;/b&gt;</xsl:text>
        <xsl:call-template name="NewLine"/>
        <xsl:text disable-output-escaping="yes">&lt;br/&gt;</xsl:text>
        <xsl:call-template name="NewLine"/>
        <xsl:text disable-output-escaping="yes">Code: $[description]</xsl:text>
        <xsl:call-template name="NewLine"/>
        <xsl:text disable-output-escaping="yes">]]&gt;</xsl:text>
      </xsl:element>
      <xsl:call-template name="NewLine"/>
    </xsl:element>
    <xsl:call-template name="NewLine"/>

  </xsl:element>
  <xsl:call-template name="NewLine"/>
</xsl:template>


<!-- **************************************************************** -->
<!-- ********************* Output a New Line ************************ -->
<!-- **************************************************************** -->
<xsl:template name="NewLine">
  <xsl:text>&#10;</xsl:text>
</xsl:template>


</xsl:stylesheet>