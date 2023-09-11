To build the UI files, use the following command:  
```
cd src/ui; pyuic6 -o mainwindow.py mainwindow.ui; pyuic6 -o addins_tab.py addins_tab.ui; pyuic6 -o options_tab.py options_tab.ui; pyuic6 -o profile_tab.py profile_tab.ui; pyuic6 -o image_display_widget.py image_display_widget.ui; cd ../..;
```
If you are a normal user, you don't have to worry about doing this. This is only necessary if you want to update the UI files.
