package com.example.jenkins;

import hudson.Extension;
import hudson.FilePath;
import hudson.Launcher;
import hudson.model.AbstractProject;
import hudson.model.Run;
import hudson.model.TaskListener;
import hudson.tasks.BuildStepDescriptor;
import hudson.tasks.Builder;
import hudson.util.FormValidation;
import jenkins.tasks.SimpleBuildStep;
import org.jenkinsci.Symbol;
import org.kohsuke.stapler.DataBoundConstructor;
import org.kohsuke.stapler.QueryParameter;

import javax.annotation.Nonnull;
import java.io.IOException;

public class SecurityAnalyzerBuilder extends Builder implements SimpleBuildStep {

    private final boolean analyzeJenkinsfile;
    private final boolean checkPlugins;
    private final String jenkinsfilePath;
    private final String jenkinsUrl;
    private final String jenkinsUser;
    private final String jenkinsToken;
    private final String nvdApiKey;

    @DataBoundConstructor
    public SecurityAnalyzerBuilder(boolean analyzeJenkinsfile, boolean checkPlugins, String jenkinsfilePath,
                                   String jenkinsUrl, String jenkinsUser, String jenkinsToken, String nvdApiKey) {
        this.analyzeJenkinsfile = analyzeJenkinsfile;
        this.checkPlugins = checkPlugins;
        this.jenkinsfilePath = jenkinsfilePath;
        this.jenkinsUrl = jenkinsUrl;
        this.jenkinsUser = jenkinsUser;
        this.jenkinsToken = jenkinsToken;
        this.nvdApiKey = nvdApiKey;
    }

    @Override
    public void perform(@Nonnull Run<?, ?> run, @Nonnull FilePath workspace, @Nonnull Launcher launcher,
                        @Nonnull TaskListener listener) throws InterruptedException, IOException {

        listener.getLogger().println("Starting Security Analysis Pipeline");

        if (analyzeJenkinsfile) {
            analyzeJenkinsfile(workspace, listener, launcher);
            generateJunitReport(workspace, listener, launcher);
        }

        if (checkPlugins) {
            checkPlugins(workspace, listener, launcher);
        }

        listener.getLogger().println("Security Analysis Pipeline Completed");
    }

    private void analyzeJenkinsfile(FilePath workspace, TaskListener listener, Launcher launcher)
            throws IOException, InterruptedException {
        listener.getLogger().println("Analyzing Jenkinsfile for security issues...");

        FilePath script = workspace.child("scripts/analyze_jenkinsfile.py");
        FilePath jenkinsfile = workspace.child(jenkinsfilePath);

        int exitCode = launcher.launch()
                .cmds("python", script.getRemote(), jenkinsfile.getRemote())
                .stdout(listener.getLogger())
                .stderr(listener.getLogger())
                .pwd(workspace)
                .join();

        if (exitCode != 0) {
            throw new RuntimeException("Jenkinsfile analysis failed with exit code " + exitCode);
        }
    }

    private void generateJunitReport(FilePath workspace, TaskListener listener, Launcher launcher)
            throws IOException, InterruptedException {
        listener.getLogger().println("Generating JUnit report from analysis...");

        FilePath script = workspace.child("scripts/generate_junit.py");

        int exitCode = launcher.launch()
                .cmds("python", script.getRemote())
                .stdout(listener.getLogger())
                .stderr(listener.getLogger())
                .pwd(workspace)
                .join();

        if (exitCode != 0) {
            throw new RuntimeException("JUnit report generation failed with exit code " + exitCode);
        }
    }

    private void checkPlugins(FilePath workspace, TaskListener listener, Launcher launcher)
            throws IOException, InterruptedException {
        listener.getLogger().println("Checking installed plugins for CVEs...");

        FilePath script = workspace.child("scripts/plugin_check.py");

        int exitCode = launcher.launch()
                .cmds("python", script.getRemote(), jenkinsUrl, jenkinsUser, jenkinsToken, nvdApiKey)
                .stdout(listener.getLogger())
                .stderr(listener.getLogger())
                .pwd(workspace)
                .join();

        if (exitCode != 0) {
            throw new RuntimeException("Plugin check failed with exit code " + exitCode);
        }
    }

    // Getters for all fields
    public boolean isAnalyzeJenkinsfile() { return analyzeJenkinsfile; }
    public boolean isCheckPlugins() { return checkPlugins; }
    public String getJenkinsfilePath() { return jenkinsfilePath; }
    public String getJenkinsUrl() { return jenkinsUrl; }
    public String getJenkinsUser() { return jenkinsUser; }
    public String getJenkinsToken() { return jenkinsToken; }
    public String getNvdApiKey() { return nvdApiKey; }

    @Symbol("securityAnalyzer")
    @Extension
    public static final class DescriptorImpl extends BuildStepDescriptor<Builder> {

        public FormValidation doCheckJenkinsfilePath(@QueryParameter String value) {
            if (value == null || value.trim().isEmpty()) {
                return FormValidation.error("Please specify the Jenkinsfile path");
            }
            return FormValidation.ok();
        }

        @Override
        public boolean isApplicable(Class<? extends AbstractProject> aClass) {
            return true;
        }

        @Override
        public String getDisplayName() {
            return "Run Security Analysis Pipeline";
        }
    }
}