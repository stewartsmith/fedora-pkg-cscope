# Makefile for source rpm: cscope
# $Id$
NAME := cscope
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
