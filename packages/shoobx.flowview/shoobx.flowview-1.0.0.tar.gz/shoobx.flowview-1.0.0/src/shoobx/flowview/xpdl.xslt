<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
  xmlns:xpdl="http://www.wfmc.org/2008/XPDL2.1" xmlns="http://www.wfmc.org/2008/XPDL2.1"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="html" indent="yes" encoding="UTF-8" />

  <!-- Load external packages -->
  <xsl:variable name="ext_pkg_hrefs" select="//xpdl:ExternalPackage/@href" />
  <xsl:variable name="ext_packages" select="document($ext_pkg_hrefs)" />
  <xsl:variable name="all_processes"
    select="/xpdl:Package/xpdl:WorkflowProcesses | $ext_packages/xpdl:Package/xpdl:WorkflowProcesses" />

  <!-- Generic template to display description -->
  <xsl:template match="xpdl:Description">
    <p class="description">
      <xsl:value-of select="." />
    </p>
  </xsl:template>

  <!-- Format formal parameters with their values -->
  <xsl:template name="actual_parameters">
    <!-- xpdl:ActualParameter nodeset -->
    <xsl:param name="actual" />
    <!-- xpdl:FormalParameter nodeset -->
    <xsl:param name="formal" />

    <xsl:for-each select="$actual">
      <xsl:variable name="pos" select="position()" />
      <xsl:variable name="param_def" select="$formal[$pos]" />

      <div class="row">
        <!-- Parameter name and docs -->
        <div class="col-lg-4">
          <xsl:call-template name="param_direction">
            <xsl:with-param name="mode" select="$param_def/@Mode" />
          </xsl:call-template>
          <xsl:text> </xsl:text>
          <tt><xsl:value-of select="$param_def/@Id" /></tt>
          <p><xsl:value-of select="$param_def/@Name" /></p>

          <xsl:apply-templates select="$param_def/xpdl:Description" />
        </div>
        <!-- Parameter value (sourece code) -->
        <div class="col-lg-8">
          <pre class="source"><xsl:value-of select="." /></pre>
        </div>
      </div>
    </xsl:for-each>
  </xsl:template>

  <!-- Application -->
  <xsl:template name="activity_application">
    <xsl:variable name="app_id" select="xpdl:Implementation/xpdl:Task/xpdl:TaskApplication/@Id" />
    <xsl:variable name="app_def" select="/xpdl:Package/xpdl:Applications/xpdl:Application[@Id=$app_id]" />

      <h4><i class="fa fa-cube"></i>
        <xsl:text> </xsl:text>
        <xsl:value-of select="$app_def/@Name" />
        <xsl:text> </xsl:text>
        <small> <xsl:value-of select="$app_id" /></small>
      </h4>
      <xsl:apply-templates select="$app_def/xpdl:Description" />

      <h4>Parameters</h4>

      <xsl:call-template name="actual_parameters">
        <xsl:with-param name="actual" select="xpdl:Implementation/xpdl:Task/xpdl:TaskApplication/xpdl:ActualParameters/xpdl:ActualParameter" />
        <xsl:with-param name="formal" select="$app_def//xpdl:FormalParameter" />
      </xsl:call-template>

  </xsl:template>

  <xsl:template name="activity_script">
    <h4>
      <i class="fa fa-puzzle-piece"></i>
      <xsl:text> </xsl:text>
      Script
      <xsl:text> </xsl:text>
      <small>
        <xsl:value-of select=".//xpdl:Script/@ScriptType" />
      </small>
    </h4>
    <pre>
      <xsl:value-of select=".//xpdl:Script" />
    </pre>
  </xsl:template>


  <xsl:template name="activity_subflow">
    <xsl:variable name="sf_id" select="xpdl:Implementation/xpdl:SubFlow/@Id" />
    <xsl:variable name="sf_def" select="$all_processes/xpdl:WorkflowProcess[@Id=$sf_id]" />

      <h4><i class="fa fa-sitemap"></i>
        <xsl:text> </xsl:text>
        <xsl:value-of select="$sf_def/@Name" />
        <xsl:text> </xsl:text>
        <small> <xsl:value-of select="$sf_id" /></small>
      </h4>

      <h4>Parameters</h4>
      <xsl:call-template name="actual_parameters">
        <xsl:with-param name="actual" select="xpdl:Implementation/xpdl:SubFlow/xpdl:ActualParameters/xpdl:ActualParameter" />
        <xsl:with-param name="formal" select="$sf_def//xpdl:FormalParameter" />
      </xsl:call-template>

  </xsl:template>


  <xsl:template name="activity_event">
    <h4>
      <xsl:choose>
        <xsl:when test="xpdl:Event/xpdl:StartEvent">
          <i class="fa fa-circle-o"></i>
          Start Event
        </xsl:when>
         <xsl:when test="xpdl:Event/xpdl:EndEvent">
          <i class="fa fa-circle"></i>
          End Event
        </xsl:when>

      </xsl:choose>

    </h4>
  </xsl:template>

  <xsl:template name="activity_route">
    <xsl:variable name="gw_type" select="xpdl:Route/@GatewayType" />
    <h4>
      <xsl:choose>
        <xsl:when test="$gw_type='Parallel'">
          <i class="fa fa-code-fork"></i> Parallel Route
        </xsl:when>
        <xsl:when test="$gw_type='Exclusive'">
          <i class="fa fa-code-fork"></i> Exclusive Route
        </xsl:when>
      </xsl:choose>
      <xsl:text> </xsl:text>
    </h4>
  </xsl:template>

  <!-- Extra Attributes -->
  <xsl:template name="extattrs">
    <xsl:if test="xpdl:ExtendedAttributes/xpdl:ExtendedAttribute">
      <h4>Extended Attributes</h4>
      <xsl:for-each select="xpdl:ExtendedAttributes/xpdl:ExtendedAttribute">
      <div class="row">
        <div class="col-lg-4">
          <tt><xsl:value-of select="@Name" /></tt>
        </div>
        <div class="col-lg-8">
          <pre class="source">
            <xsl:value-of select="." />
            <xsl:value-of select="@Value" />
          </pre>
        </div>
      </div>
      </xsl:for-each>
    </xsl:if>
  </xsl:template>

  <!-- Generate link to an activity

  Available in any context
   -->
  <xsl:template name="activity-link">
    <xsl:param name="target_act_id" />
    <xsl:param name="activities" />
    <xsl:variable name="activity" select="$activities[@Id=$target_act_id]" />
    <a>
      <xsl:attribute name="href">
        #activity-<xsl:value-of select="$target_act_id" />
      </xsl:attribute>
      <xsl:choose>
        <xsl:when test="$activity/@Name">
          <xsl:value-of select="$activity/@Name" />
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$activity/@Id" />
        </xsl:otherwise>
      </xsl:choose>
    </a>
  </xsl:template>

  <!-- Render transition information
  -->
  <xsl:template name="transition" match="xpdl:Transition">
    <xsl:param name="target_act_id" />
    <xsl:param name="activities" />

    <xsl:call-template name="activity-link">
      <xsl:with-param name="target_act_id" select="$target_act_id" />
      <xsl:with-param name="activities" select="$activities" />
    </xsl:call-template>

    <xsl:choose>
      <xsl:when test="xpdl:Condition[@Type='CONDITION']">
        when <code><xsl:value-of select="xpdl:Condition" /></code>
      </xsl:when>
      <xsl:when test="xpdl:Condition[@Type='OTHERWISE']">
        otherwise
      </xsl:when>
    </xsl:choose>

    via
    <tt><xsl:value-of select="@Id" /></tt>

    <xsl:if test="@Name or xpdl:Description">
      <p class="description">
        <xsl:if test="@Name">
          <b><xsl:value-of select="@Name" />.</b>
          <xsl:text> </xsl:text>
        </xsl:if>
        <xsl:value-of select="xpdl:Description" />
      </p>
    </xsl:if>

  </xsl:template>

  <xsl:template name="transitions">
    <xsl:variable name="transitions" select="../../xpdl:Transitions/xpdl:Transition" />
    <xsl:variable name="activities" select="../xpdl:Activity" />
    <xsl:variable name="act_id" select="@Id" />

    <div class="row">
      <div class="col-lg-6">
        <xsl:for-each select="$transitions[@From=$act_id]">
          <div>
            <i class="fa fa-long-arrow-right"></i>
            <xsl:text> </xsl:text>
            <xsl:call-template name="transition">
              <xsl:with-param name="target_act_id" select="@To" />
              <xsl:with-param name="activities" select="$activities" />
            </xsl:call-template>
          </div>
        </xsl:for-each>
      </div>
      <div class="col-lg-6">
        <xsl:for-each select="$transitions[@To=$act_id]">
          <div>
            <i class="fa fa-long-arrow-left"></i>
            <xsl:text> </xsl:text>
            <xsl:call-template name="transition">
              <xsl:with-param name="target_act_id" select="@From" />
              <xsl:with-param name="activities" select="$activities" />
            </xsl:call-template>
          </div>
        </xsl:for-each>
      </div>

    </div>
  </xsl:template>


  <!-- Activity -->
  <xsl:template name="activity">
    <h3>
      <xsl:attribute name="id">activity-<xsl:value-of select="@Id" /></xsl:attribute>
      <xsl:value-of select="@Name" />
      <xsl:text> </xsl:text>
      <small> <xsl:value-of select="@Id" /></small>
    </h3>
    <xsl:call-template name="transitions" />

    <div class="activity-info">
      <xsl:choose>
        <xsl:when test="xpdl:Implementation/xpdl:Task/xpdl:TaskApplication">
          <xsl:call-template name="activity_application" />
        </xsl:when>
        <xsl:when test="xpdl:Implementation/xpdl:Task/xpdl:TaskScript">
          <xsl:call-template name="activity_script" />
        </xsl:when>
        <xsl:when test="xpdl:Implementation/xpdl:SubFlow">
          <xsl:call-template name="activity_subflow" />
        </xsl:when>
        <xsl:when test="xpdl:Event">
          <xsl:call-template name="activity_event" />
        </xsl:when>
        <xsl:when test="xpdl:Route">
          <xsl:call-template name="activity_route" />
        </xsl:when>
      </xsl:choose>
      <xsl:call-template name="extattrs" />
    </div>

  </xsl:template>

  <xsl:template name="param_direction">
    <xsl:param name="mode" />
    <xsl:choose>
      <xsl:when test="$mode='IN'">
        <i class="fa fa-arrow-right"></i>
      </xsl:when>
      <xsl:when test="$mode='OUT'">
        <i class="fa fa-arrow-left"></i>
      </xsl:when>
      <xsl:when test="$mode='INOUT'">
        <i class="fa fa-arrow-left"></i>
        <i class="fa fa-arrow-right"></i>
      </xsl:when>
    </xsl:choose>
  </xsl:template>

  <!-- Process formal parameters -->
  <xsl:template name="formal_parameters">
    <h4>Formal parameters</h4>
    <ul>
      <xsl:for-each select="xpdl:FormalParameters/xpdl:FormalParameter">
        <li>
          <xsl:call-template name="param_direction">
            <xsl:with-param name="mode" select="@Mode" />
          </xsl:call-template>
          <xsl:text> </xsl:text>
          <tt>
            <xsl:value-of select="@Id" />
            <xsl:if test="xpdl:InitialValue">=<xsl:value-of select="xpdl:InitialValue" />
            </xsl:if>
          </tt>

          <p><xsl:value-of select="@Name" /></p>
          <xsl:apply-templates select="xpdl:Description" />
        </li>
      </xsl:for-each>
    </ul>
  </xsl:template>

  <xsl:template name="workflow_variables">
    <h4>Workflow Variables</h4>
    <ul>
      <xsl:for-each select="xpdl:DataFields/xpdl:DataField">
        <li>
          <tt>
            <xsl:value-of select="@Id" />
            <xsl:if test="xpdl:InitialValue">=<xsl:value-of select="xpdl:InitialValue" />
            </xsl:if>
          </tt>

          <p><xsl:value-of select="@Name" /></p>
          <xsl:apply-templates select="xpdl:Description" />
        </li>
      </xsl:for-each>
    </ul>
  </xsl:template>

  <!-- Process definition -->
  <xsl:template name="process">
    <h2>
      <xsl:attribute name="id">process-<xsl:value-of select="@Id" /></xsl:attribute>
      <xsl:value-of select="@Name" />
      <xsl:text> </xsl:text>
      <small> <xsl:value-of select="@Id" /></small>
    </h2>

    <div class="process-info">
      <div class="row">
        <div class="col-lg-6">
          <xsl:call-template name="formal_parameters" />
        </div>
        <div class="col-lg-6">
          <xsl:call-template name="workflow_variables" />
        </div>
      </div>
      <xsl:call-template name="extattrs" />
    </div>

    <xsl:for-each select="xpdl:Activities/xpdl:Activity">
          <xsl:call-template name="activity" />
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="nav-package">
    <ul class="nav nav-list">
      <xsl:for-each select="//xpdl:WorkflowProcesses/xpdl:WorkflowProcess">
        <li>
          <a>
            <xsl:attribute name="href">#process-<xsl:value-of select="@Id" /></xsl:attribute>
            <xsl:value-of select="@Name" />
          </a>
          <ul class="nav nxav-list">
            <xsl:for-each select="xpdl:Activities/xpdl:Activity">
              <li>
                <a>
                  <xsl:attribute name="href">#activity-<xsl:value-of select="@Id" /></xsl:attribute>
                  <xsl:value-of select="@Name" />
                </a>
              </li>
            </xsl:for-each>
          </ul>
        </li>
      </xsl:for-each>
    </ul>
  </xsl:template>

  <xsl:template name="navigation">
    <ul class="nav nav-list">
      <li>
        <a>
          <xsl:attribute name="href">#package-<xsl:value-of select="@Id" /></xsl:attribute>
          <xsl:value-of select="//xpdl:Package/@Name" />
        </a>
        <xsl:call-template name="nav-package" />
      </li>
      <xsl:for-each select="$ext_packages">
        <li>
          <a>
            <xsl:attribute name="href">#package-<xsl:value-of select="xpdl:Package/@Id" /></xsl:attribute>
            <xsl:value-of select="//xpdl:Package/@Name" />
          </a>
          <xsl:call-template name="nav-package" />
        </li>
      </xsl:for-each>

    </ul>
  </xsl:template>

  <xsl:template name="package">
    <h1>
      <xsl:attribute name="id">package-<xsl:value-of select="@Id" /></xsl:attribute>
      <xsl:value-of select="//xpdl:Package/@Name" />
      <xsl:text> </xsl:text>
      <small><xsl:value-of select="//xpdl:Package/@Id" /></small>
    </h1>

    <xsl:for-each select="//xpdl:WorkflowProcesses/xpdl:WorkflowProcess">
      <xsl:call-template name="process" />
    </xsl:for-each>
  </xsl:template>

  <xsl:include href="flowview:layout.xslt" />

  <xsl:template match="/">
    <xsl:call-template name="layout">
      <xsl:with-param name="title">
        <xsl:value-of select="//xpdl:Package/@Name" />
      </xsl:with-param>

      <xsl:with-param name="contents">
        <xsl:call-template name="package" />

        <xsl:for-each select="$ext_packages/xpdl:Package">
          <xsl:call-template name="package" />
        </xsl:for-each>
      </xsl:with-param>

      <xsl:with-param name="navigation">
          <xsl:call-template name="navigation" />
      </xsl:with-param>

    </xsl:call-template>
  </xsl:template>

</xsl:stylesheet>