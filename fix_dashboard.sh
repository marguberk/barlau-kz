#!/bin/bash
head -n -1 core/templates/core/dashboard.html > dashboard.html.tmp
echo "</script>" >> dashboard.html.tmp
echo "</html>" >> dashboard.html.tmp
mv dashboard.html.tmp core/templates/core/dashboard.html
