<?xml version="1.0" encoding="ISO-8859-1" standalone="no"?>
<xsl:stylesheet version="1.0"    
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" >
	<!-- (c) 2005, Trimble Navigation Limited. All rights reserved.                                -->
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
	<xsl:variable name="DecPt" select="'.'"/>
	<!-- Change as appropriate for US/European -->
	<xsl:variable name="GroupSep" select="','"/>
	<!-- Change as appropriate for US/European -->
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
	<xsl:variable name="DecPl11" select="concat('#0', $DecPt, '00000000000')"/>
	<xsl:variable name="DecPl14" select="concat('#0', $DecPt, '00000000000000')"/>
	<xsl:variable name="fileExt" select="'gpx'"/>
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
		<xsl:value-of select="'&lt;?xml version=&quot;1.0&quot; encoding=&quot;ISO-8859-1&quot; standalone=&quot;yes&quot;?&gt;'"/>
		<xsl:call-template name="NewLine"/>
		
		<xsl:value-of select="'&lt;gpx'"/>
		<xsl:call-template name="NewLine"/>
		<xsl:value-of select="'xmlns=&quot;http://www.trimble.com&quot;'"/>
		<xsl:call-template name="NewLine"/>
        <xsl:value-of select="'version=&quot;1.1&quot;'"/>
        <xsl:call-template name="NewLine"/>
        <xsl:value-of select="'creator=&quot;Trimble Survey Controller&quot;'"/>
        <xsl:call-template name="NewLine"/>
        <xsl:value-of select="'xmlns:xsi=&quot;http://www.trimble.com&quot;'"/>
        <xsl:call-template name="NewLine"/>
        <xsl:value-of select="'xsi:schemaLocation=&quot;http://www.trimble.com&quot;&gt;'"/>
        <xsl:call-template name="NewLine"/>
	    <xsl:value-of select="'    &lt;metadata&gt;'"/>
	    <xsl:call-template name="NewLine"/>
		<xsl:value-of select="concat('        &lt;name&gt;',JOBFile/@jobName, '.jxl&lt;/name&gt;')"/>
		<xsl:call-template name="NewLine"/>
		<xsl:value-of select="concat('        &lt;desc&gt;',JOBFile/@jobName, '.jxl&lt;/desc&gt;')"/>
		<xsl:call-template name="NewLine"/>
		
		<xsl:value-of select="'        &lt;link href=&quot;http://www.trimble.com&quot;&gt;'"/>
		<xsl:call-template name="NewLine"/>
		<xsl:value-of select="'            &lt;text&gt;Trimble Navigation Ltd.&lt;/text&gt;'"/>
		<xsl:call-template name="NewLine"/>
		<xsl:value-of select="'        &lt;/link&gt;'"/>
		<xsl:call-template name="NewLine"/>
		<xsl:value-of select="'    &lt;/metadata&gt;'"/>
		<xsl:call-template name="NewLine"/>
	
	
		<xsl:apply-templates select="JOBFile/Reductions" />
		<xsl:value-of select="'    &lt;extensions&gt;&lt;/extensions&gt;'"/>
		<xsl:call-template name="NewLine"/>
		<xsl:value-of select="'&lt;/gpx&gt;'"/>
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
	<xsl:template match="Point">
		<xsl:if test="WGS84">
		    <xsl:value-of select="concat('    &lt;wpt lat=&quot;', WGS84/Latitude, '&quot; lon=&quot;', WGS84/Longitude, '&quot;&gt;')"/>
		    <xsl:call-template name="NewLine"/>
		    <xsl:value-of select="concat('        &lt;ele&gt;', format-number(WGS84/Height, $DecPl2, 'Standard'), '&lt;/ele&gt;')"/>
		    <xsl:call-template name="NewLine"/>
		    <xsl:value-of select="concat('        &lt;name&gt;', Name, '&lt;/name&gt;')"/>
		    <xsl:call-template name="NewLine"/>
		   
		    <xsl:value-of select="'    &lt;/wpt&gt;'"/>
		    <xsl:call-template name="NewLine"/>		
		</xsl:if>
	</xsl:template>
	<!-- **************************************************************** -->
	<!-- ********************* Blank Line Output ************************ -->
	<!-- **************************************************************** -->
	<xsl:template name="BlankLine">
		<xsl:call-template name="NewLine"/>
		<xsl:call-template name="NewLine"/>
	</xsl:template>
	<!-- **************************************************************** -->
	<!-- ********************** New Line Output ************************* -->
	<!-- **************************************************************** -->
	<xsl:template name="NewLine">
		<xsl:text>&#10;</xsl:text>
	</xsl:template>
	<!-- **************************************************************** -->
	<!-- *********** Pad a string to the right with spaces ************** -->
	<!-- **************************************************************** -->
	<xsl:template name="PadRight">
		<xsl:param name="StringWidth"/>
		<xsl:param name="TheString"/>
		<xsl:choose>
			<xsl:when test="$StringWidth = '0'">
				<xsl:value-of select="normalize-space($TheString)"/>
				<!-- Function return value -->
			</xsl:when>
			<xsl:otherwise>
				<xsl:variable name="PaddedStr" select="concat($TheString, '                                       ')"/>
				<xsl:value-of select="substring($PaddedStr, 1, $StringWidth)"/>
				<!-- Function return value -->
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<!-- **************************************************************** -->
	<!-- *********** Pad a string to the left with spaces *************** -->
	<!-- **************************************************************** -->
	<xsl:template name="PadLeft">
		<xsl:param name="StringWidth"/>
		<xsl:param name="TheString"/>
		<xsl:choose>
			<xsl:when test="$StringWidth = '0'">
				<xsl:value-of select="normalize-space($TheString)"/>
			</xsl:when>
			<xsl:otherwise>
				<xsl:variable name="PaddedStr" select="concat('                                       ', $TheString)"/>
				<xsl:value-of select="substring($PaddedStr, string-length($PaddedStr) - $StringWidth + 1)"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>