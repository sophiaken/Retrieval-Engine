<%-- 
    Document   : candidatelogin
    Created on : Feb 21, 2016, 1:23:25 PM
    Author     : Acer
--%>

<%@page import="java.lang.String"%>
<%@page import="bean.BeanClass"%>
<%@page import="dao.DataAccess"%>
<%@page import="java.util.List"%>
<%@page import="java.util.LinkedList"%>
<%@page contentType="text/html" pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%-- 
    Document   : masterpage
    Created on : Feb 21, 2016, 1:21:33 PM
    Author     : Acer
--%>

<html lang="en">
  <head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Candidatelogin</title>
  <!-- Bootstrap -->
  <link href="css/bootstrap.css" rel="stylesheet">
  <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
  <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
  <!--[if lt IE 9]>
		  <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
		  <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
		<![endif]-->
  <link rel="stylesheet" type="text/css" href="fontawesome/css/font-awesome.min.css" />
  <link rel="stylesheet" type="text/css" href="js/lightbox/css/lightbox.min.css">
  <link href="css/style.css" rel="stylesheet" type="text/css">

  <!--The following script tag downloads a font from the Adobe Edge Web Fonts server for use within the web page. We recommend that you do not modify it.--><script>var __adobewebfontsappname__="dreamweaver"</script><script src="http://use.edgefonts.net/open-sans:n3,n4:default.js" type="text/javascript"></script>
</head>
  <body>
                        <%
                       
                        String username = (String) session.getAttribute("password"); 
                        if(username!=null){
                        %>	
  <nav class="navbar navbar-fixed-top">
  	<div class="container">
  		<!-- Brand and toggle get grouped for better mobile display -->
  		<div class="navbar-header">
  			<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#topFixedNavbar1" aria-expanded="false"><span class="sr-only">Toggle navigation</span><span class="icon-bar"></span><span class="icon-bar"></span><span class="icon-bar"></span></button>
  			<a class="navbar-brand text-uppercase" href="#">YOUR RIGHTS</a></div>
  		<!-- Collect the nav links, forms, and other content for toggling -->
  		<div class="collapse navbar-collapse" id="topFixedNavbar1">
			<ul class="nav navbar-nav navbar-right text-uppercase">
  			
                        <li style="color:#ffffff"><% out.println(username); %></li>
  				
  				
  				
			</ul>
		</div> 
  		<!-- /.navbar-collapse -->
	  </div>
  	<!-- /.container-fluid -->
  </nav>
  
  <div id="carousel1" class="carousel slide" data-ride="carousel">
  	<ol class="carousel-indicators">
  		<li data-target="#carousel1" data-slide-to="0" class="active"></li>
  		<li data-target="#carousel1" data-slide-to="1"></li>
  		<li data-target="#carousel1" data-slide-to="2"></li>
	  </ol>
  	<div class="carousel-inner" role="listbox">
  		<div class="item active">
			<img src="images/carousel.jpg" alt="First slide image" class="center-block">
  			<div class="carousel-caption">
                            <style>
.spc{
width:40px;
height: 50px;
}          
.formstyle{
    background-color: #bdb76b;
    width: 600px;
    height: 800px;
    border:1px solid blueviolet;
    margin-left: 400px;
    padding: 10px;

}
.radiobtn{
    width: 20px;
    height: 20px;
}
.butn{
    width: 100px;
    height: 40px;
    background-color:  seagreen;
    color:white;
    border-radius: 5px;
    border: 1px solid seagreen;
}

                            </style>
                                
                                
           
                                    <form class="formstyle" action="PartyVote" method="post">
                                       <% 
                                    request.setAttribute("Allpost", DataAccess.fetchQuery(username));
                                         %>
                                         <br><br> <br><br> 
                                        <table cellspacing="10">
                                            <c:forEach items="${Allpost}" var="p">
                                            <tr>
                                                <td >AatharID :</td>
                                                  <td >${p.aatharid}</td>
                                            </tr>
                                            <tr>
                                                <td>Voter ID :</td>
                                                  <td>${p.voterid}</td>
                                            </tr>
                                            <tr>
                                                <td>Name :</td>
                                                  <td>${p.name}</td>
                                            </tr>
                                            <tr>
                                                <td>DOB :</td>
                                                  <td>${p.dob}</td>
                                            </tr>
                                               <tr>
                                            <td>Age :</td>
                                              <td>${p.age}</td>
                                            </tr>
                                            <tr>
                                                <td>City :</td>
                                                  <td>${p.city}</td>
                                            </tr>
                                            <tr>
                                                <td>Area :</td>
                                                  <td>${p.area}</td>
                                            </tr>
                                            <tr>
                                                <td>Ward no :</td>
                                                  <td>${p.wardno}</td>
                                            </tr>
                                            </c:forEach>
                                        </table> 
                                         <br> 
                                        <h3>Choose Your Party</h3>
                                        <center>  
                                <table cellspacing="10">
                                    <tr>
                                        <td class="spc"> <input class="radiobtn" type="radio" value="party1" name="party"></td><td>PARTY-1</td>
                                    </tr>
                                    <tr>
                                        <td class="spc"> <input class="radiobtn" type="radio" value="party2" name="party"></td><td>PARTY-2</td>
                                    </tr>
                                    <tr>
                                        <td class="spc"> <input class="radiobtn" type="radio" value="party3" name="party"></td><td>PARTY-3</td>
                                    </tr>
                                    <tr>
                                        <td class="spc"> <input class="radiobtn" type="radio" value="party4" name="party"></td><td>PARTY-4</td>
                                    </tr>
                                    <tr>
                                        </td><td>
                                <td> <input class="butn" type="submit" value="Submit"/>   </td>
                                    </tr>
                                </table>
                                </center>  
                                        

                               
                            </form> 
                            
                                    
                                
                                
			</div>
                        
			<!-- / carousel-caption -->
		</div>
		<!--/ item-->
  		
	  </div>
	  
  
  <footer class="footer container-fluid text-center">
  	<div class="logo"><span>Your rights</span></div>
	<div class="socials">
		<a href="#"><span class="fa fa-facebook"></span></a>
		<a href="#"><span class="fa fa-twitter"></span></a>
		<a href="#"><span class="fa fa-google-plus"></span></a>
	</div>
	<p>&copy; 2015, by your rights reserved</p>
	<!--you must keep the link bellow, you are not allowed to remove it, if you want to remove it please contact us at aythemes.com/contact -->
	
  </footer>
<% }else {
                                out.println("<script type=\"text/javascript\">");
                                out.println("alert('Access is denied. Please login fist!...')");
                                out.println("location='index.html'");
                                out.println("</script>");
                        }%>
  </body>
</html>