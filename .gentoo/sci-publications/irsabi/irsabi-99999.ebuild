# Copyright 1999-2019 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2

EAPI=7

PYTHON_COMPAT=( python{2_7,3_4,3_5,3_6} )

DESCRIPTION="Registration Workflow and Geometric Space for Small Animal Brain Imaging"
HOMEPAGE="https://bitbucket.org/TheChymera/irsabi"

LICENSE="GPL-3"
SLOT="0"
IUSE="-scanner-data"
KEYWORDS=""

DEPEND=""
RDEPEND="
	dev-python/matplotlib
	dev-python/numpy
	dev-python/pandas
	>=dev-python/statsmodels-0.9.0
	>=dev-tex/pythontex-0.16
	dev-texlive/texlive-latex
	media-gfx/graphviz
	sci-biology/nilearn
	scanner-data? ( sci-biology/samri_data )
	!scanner-data? ( sci-biology/samri_bidsdata )
"
