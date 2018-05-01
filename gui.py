# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jan 23 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class BlenFloat
###########################################################################

class BlenFloat ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"BlenFloat", pos = wx.DefaultPosition, size = wx.Size( 385,384 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		bSizer4 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_panel1 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer5 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizer6.SetMinSize( wx.Size( -1,50 ) ) 
		self.m_button2 = wx.Button( self.m_panel1, wx.ID_ANY, u"export", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button2, 0, wx.ALL, 5 )
		
		self.m_button4 = wx.Button( self.m_panel1, wx.ID_ANY, u"F", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		bSizer6.Add( self.m_button4, 0, wx.ALL, 5 )
		
		self.m_button5 = wx.Button( self.m_panel1, wx.ID_ANY, u"undo", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button5, 0, wx.ALL, 5 )
		
		self.m_button6 = wx.Button( self.m_panel1, wx.ID_ANY, u"redo", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer6.Add( self.m_button6, 0, wx.ALL, 5 )
		
		
		bSizer5.Add( bSizer6, 1, wx.EXPAND, 5 )
		
		sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"label" ), wx.VERTICAL )
		
		fgSizer1 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText1 = wx.StaticText( sbSizer1.GetStaticBox(), wx.ID_ANY, u"Polygons count 2K default", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
		
		self.text_remesh = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, u"2", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
		fgSizer1.Add( self.text_remesh, 0, wx.ALL, 5 )
		
		self.m_button9 = wx.Button( sbSizer1.GetStaticBox(), wx.ID_ANY, u"remesh", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_button9, 0, wx.ALL, 5 )
		
		
		sbSizer1.Add( fgSizer1, 1, wx.EXPAND, 5 )
		
		
		bSizer5.Add( sbSizer1, 1, wx.EXPAND, 5 )
		
		sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel1, wx.ID_ANY, u"label" ), wx.VERTICAL )
		
		fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText2 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, u"Resolution 128", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer2.Add( self.m_staticText2, 0, wx.ALL, 5 )
		
		self.text_dynamesh = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, u"128", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.text_dynamesh, 0, wx.ALL, 5 )
		
		self.m_button10 = wx.Button( sbSizer2.GetStaticBox(), wx.ID_ANY, u"dynamesh", wx.Point( 0,100 ), wx.DefaultSize, 0 )
		fgSizer2.Add( self.m_button10, 0, wx.ALL, 5 )
		
		
		sbSizer2.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		
		bSizer5.Add( sbSizer2, 1, wx.EXPAND, 5 )
		
		
		bSizer5.Add( ( 0, 100), 1, wx.EXPAND, 5 )
		
		self.m_staticText3 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"zsc path zbrush/ZScripts", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )
		bSizer5.Add( self.m_staticText3, 0, wx.ALL, 5 )
		
		self.text_zsc = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"D:/apps/Pixologic ZBrush V4R7 P2 Portable/Picologic ZBrush 4R7 P2/ZScripts", wx.DefaultPosition, wx.Size( 300,-1 ), 0 )
		bSizer5.Add( self.text_zsc, 0, wx.ALL, 5 )
		
		
		self.m_panel1.SetSizer( bSizer5 )
		self.m_panel1.Layout()
		bSizer5.Fit( self.m_panel1 )
		self.m_notebook1.AddPage( self.m_panel1, u"Gob", True )
		self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer41 = wx.BoxSizer( wx.VERTICAL )
		
		self.m_button51 = wx.Button( self.m_panel2, wx.ID_ANY, u"Run test.py", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer41.Add( self.m_button51, 0, wx.ALL, 5 )
		
		
		self.m_panel2.SetSizer( bSizer41 )
		self.m_panel2.Layout()
		bSizer41.Fit( self.m_panel2 )
		self.m_notebook1.AddPage( self.m_panel2, u"Rig", False )
		
		bSizer4.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizer4 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_button2.Bind( wx.EVT_BUTTON, self.on_export )
		self.m_button9.Bind( wx.EVT_BUTTON, self.on_remesh )
		self.m_button10.Bind( wx.EVT_BUTTON, self.on_dynamesh )
		self.m_button51.Bind( wx.EVT_BUTTON, self.on_run_test_py )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def on_export( self, event ):
		event.Skip()
	
	def on_remesh( self, event ):
		event.Skip()
	
	def on_dynamesh( self, event ):
		event.Skip()
	
	def on_run_test_py( self, event ):
		event.Skip()
	

