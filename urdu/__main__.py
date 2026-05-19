"""Allow running as: python -m urdu"""
import sys
try:
    from urdu.cli import main
except ImportError:
    from .cli import main
sys.exit(main())
