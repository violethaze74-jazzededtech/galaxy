from ..base.twilltestcase import (
    common,
    ShedTwillTestCase,
)

column_maker_repository_name = "column_maker_0020"
column_maker_repository_description = "A flexible aligner."
column_maker_repository_long_description = "A flexible aligner and methylation caller for Bisulfite-Seq applications."

emboss_repository_name = "emboss_0020"
emboss_repository_description = "Galaxy wrappers for Emboss version 5.0.0 tools for test 0020"
emboss_repository_long_description = "Galaxy wrappers for Emboss version 5.0.0 tools for test 0020"


class ToolWithRepositoryDependencies(ShedTwillTestCase):
    """Test installing a repository with repository dependencies."""

    def test_0000_initiate_users(self):
        """Create necessary user accounts."""
        self.login(email=common.test_user_1_email, username=common.test_user_1_name)
        test_user_1 = self.test_db_util.get_user(common.test_user_1_email)
        assert (
            test_user_1 is not None
        ), f"Problem retrieving user with email {common.test_user_1_email} from the database"
        self.test_db_util.get_private_role(test_user_1)
        self.login(email=common.admin_email, username=common.admin_username)
        admin_user = self.test_db_util.get_user(common.admin_email)
        assert admin_user is not None, f"Problem retrieving user with email {common.admin_email} from the database"
        self.test_db_util.get_private_role(admin_user)
        self.galaxy_login(email=common.admin_email, username=common.admin_username)
        galaxy_admin_user = self.test_db_util.get_galaxy_user(common.admin_email)
        assert (
            galaxy_admin_user is not None
        ), f"Problem retrieving user with email {common.admin_email} from the database"
        self.test_db_util.get_galaxy_private_role(galaxy_admin_user)

    def test_0005_ensure_repositories_and_categories_exist(self):
        """Create the 0020 category and any missing repositories."""
        category = self.create_category(
            name="Test 0020 Basic Repository Dependencies", description="Test 0020 Basic Repository Dependencies"
        )
        self.login(email=common.test_user_1_email, username=common.test_user_1_name)
        column_maker_repository = self.get_or_create_repository(
            name=column_maker_repository_name,
            description=column_maker_repository_description,
            long_description=column_maker_repository_long_description,
            owner=common.test_user_1_name,
            category_id=self.security.encode_id(category.id),
            strings_displayed=[],
        )
        if self.repository_is_new(column_maker_repository):
            self.upload_file(
                column_maker_repository,
                filename="column_maker/column_maker.tar",
                filepath=None,
                valid_tools_only=True,
                uncompress_file=True,
                remove_repo_files_not_in_tar=False,
                commit_message="Uploaded column_maker tarball.",
                strings_displayed=[],
                strings_not_displayed=[],
            )
            emboss_repository = self.get_or_create_repository(
                name=emboss_repository_name,
                description=emboss_repository_description,
                long_description=emboss_repository_long_description,
                owner=common.test_user_1_name,
                category_id=self.security.encode_id(category.id),
                strings_displayed=[],
            )
            self.upload_file(
                emboss_repository,
                filename="emboss/emboss.tar",
                filepath=None,
                valid_tools_only=True,
                uncompress_file=True,
                remove_repo_files_not_in_tar=False,
                commit_message="Uploaded emboss.tar",
                strings_displayed=[],
                strings_not_displayed=[],
            )
            repository_dependencies_path = self.generate_temp_path("test_1020", additional_paths=["emboss", "5"])
            repository_tuple = (
                self.url,
                column_maker_repository.name,
                column_maker_repository.user.username,
                self.get_repository_tip(column_maker_repository),
            )
            self.create_repository_dependency(
                repository=emboss_repository,
                repository_tuples=[repository_tuple],
                filepath=repository_dependencies_path,
            )

    def test_0010_browse_tool_shed(self):
        """Browse the available tool sheds in this Galaxy instance and preview the emboss tool."""
        self.galaxy_login(email=common.admin_email, username=common.admin_username)
        self.browse_tool_shed(url=self.url, strings_displayed=["Test 0020 Basic Repository Dependencies"])
        category = self.test_db_util.get_category_by_name("Test 0020 Basic Repository Dependencies")
        self.browse_category(category, strings_displayed=["emboss_0020"])
        self.preview_repository_in_tool_shed(
            "emboss_0020", common.test_user_1_name, strings_displayed=["emboss_0020", "Valid tools"]
        )

    def test_0015_install_emboss_repository(self):
        """Install the emboss repository without installing tool dependencies."""
        strings_displayed = ["Handle", "Never installed", "tool dependencies", "emboss", "5.0.0", "package"]
        self.install_repository(
            "emboss_0020",
            common.test_user_1_name,
            "Test 0020 Basic Repository Dependencies",
            strings_displayed=strings_displayed,
            install_tool_dependencies=False,
            new_tool_panel_section_label="test_1020",
        )
        installed_repository = self.test_db_util.get_installed_repository_by_name_owner(
            "emboss_0020", common.test_user_1_name
        )
        strings_displayed = [
            "emboss_0020",
            "Galaxy wrappers for Emboss version 5.0.0 tools for test 0020",
            "user1",
            self.url.replace("http://", ""),
            installed_repository.installed_changeset_revision,
        ]
        self.display_galaxy_browse_repositories_page(strings_displayed=strings_displayed)
        strings_displayed.extend(["Installed tool shed repository", "Valid tools", "antigenic"])
        self.display_installed_repository_manage_page(installed_repository, strings_displayed=strings_displayed)
        self.verify_tool_metadata_for_installed_repository(installed_repository)

    def test_0020_verify_installed_repository_metadata(self):
        """Verify that resetting the metadata on an installed repository does not change the metadata."""
        self.verify_installed_repository_metadata_unchanged("emboss_0020", common.test_user_1_name)

    def test_0025_deactivate_datatypes_repository(self):
        """Deactivate the emboss_datatypes repository without removing it from disk."""
        installed_repository = self.test_db_util.get_installed_repository_by_name_owner(
            column_maker_repository_name, common.test_user_1_name
        )
        self.deactivate_repository(installed_repository)

    def test_0030_reactivate_datatypes_repository(self):
        """Reactivate the datatypes repository and verify that the datatypes are again present."""
        installed_repository = self.test_db_util.get_installed_repository_by_name_owner(
            column_maker_repository_name, common.test_user_1_name
        )
        self.reactivate_repository(installed_repository)
        # This used to reactive datatype repositories and verify counts...
        # test may be considerably less useful now.
