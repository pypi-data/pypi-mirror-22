<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
  xmlns:xpdl="http://www.wfmc.org/2008/XPDL2.1" xmlns="http://www.wfmc.org/2008/XPDL2.1"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:template name="layout">
    <xsl:param name="title" />
    <xsl:param name="contents" />
    <xsl:param name="navigation" />

    <html>
      <head>
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css" />

        <!-- Optional theme -->
        <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap-theme.min.css" />

        <link href="https://netdna.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet" />

        <title><xsl:value-of select="$title" /> - FlowView</title>

        <style>
          <xsl:value-of select="document('flowview:flowview.css')/style"
            disable-output-escaping="yes"/>
        </style>
      </head>
      <body data-spy="scroll" data-target=".sidenav">
        <div class="navbar navbar-inverse" role="navigation">
          <div class="container">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="#">FlowView</a>
            </div>
            <div class="navbar-collapse collapse">
              <form class="navbar-form navbar-right" role="form">
                <div class="form-group">
                  <input type="text" id="baseurl" placeholder="App URL" class="form-control baseurl" />
                </div>
              </form>
              <div class="navbar-right">
                <p class="navbar-text">App URL</p>
              </div>
            </div><!--/.navbar-collapse -->
          </div>
        </div>

        <div class="container">
          <div class="row">
            <div class="col-lg-10">
              <xsl:copy-of select="$contents" />
            </div>
            <div class="col-lg-2">
              <div class="sidenav " data-spy="affix" data-offset-top="0" data-offset-bottom="200">
                <xsl:copy-of select="$navigation" />
              </div>
            </div>

          </div>
        </div>

        <!-- Latest compiled and minified JavaScript -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js">;</script>
        <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js">;</script>

        <script src="tags.js">;</script>

        <script type="text/javascript">
          <xsl:value-of select="document('flowview:flowview.js')/script"
            disable-output-escaping="yes"/>
        </script>

      </body>
    </html>


  </xsl:template>

</xsl:stylesheet>