# lint-amnesty, pylint: disable=missing-module-docstring

import logging

from web_fragments.fragment import Fragment
from xblock.core import XBlock
from xblock.fields import Scope, String

from xmodule.x_module import (
    XModuleMixin,
    XModuleToXBlockMixin,
)
from xmodule.xml_block import XmlMixin

log = logging.getLogger(__name__)

# Make '_' a no-op so we can scrape strings
_ = lambda text: text


@XBlock.needs("mako")
class GameBlock(  # lint-amnesty, pylint: disable=abstract-method
    XmlMixin,
    XModuleToXBlockMixin,
    XModuleMixin,
    XBlock,
):
    """
    Game XBlock for displaying interactive game content in courses.
    This is a read-only component for students to view game content.
    """

    display_name = String(
        display_name=_("Display Name"),
        help=_("The display name for this component."),
        scope=Scope.settings,
        default=_("Game")
    )

    game_type = String(
        help=_("Type of game"),
        display_name=_("Game Type"),
        default="",
        scope=Scope.settings
    )

    data = String(
        help=_("Game content to display for this block"),
        default="",
        scope=Scope.content
    )

    @XBlock.supports("multi_device")
    def student_view(self, _context):
        """
        Return a fragment that contains the html for the student view
        """
        from xmodule.util.builtin_assets import add_css_to_fragment

        context = {
            'game_type': self.game_type,
            'data': self.data if self.data else ""
        }
        fragment = Fragment(
            self.runtime.service(self, 'mako').render_lms_template('game.html', context)
        )
        add_css_to_fragment(fragment, 'GameBlockDisplay.css')
        return fragment

    @XBlock.supports("multi_device")
    def public_view(self, context):
        """
        Returns a fragment that contains the html for the preview view
        """
        return self.student_view(context)
